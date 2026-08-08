"""
Final assessment - Section B - Question 4

Task aim:
Use the FDA AI Medical Devices dataset to forecast monthly authorization
counts. NumPy and Pandas prepare the time series, Scikit-learn scales and
evaluates it, and TensorFlow/Keras builds SimpleRNN, LSTM and GRU models.
"""

# 1. Importing Libraries
import warnings
warnings.filterwarnings("ignore")

import os
import random
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, LSTM, GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)
sns.set_style("whitegrid")

# Always use the folder containing this Python file as the working folder.
# This prevents FileNotFoundError when VS Code starts the script elsewhere.
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

os.makedirs("outputs/Question_4", exist_ok=True)


# 2. Loading the FDA Dataset
data = pd.read_csv("data/fda/fda_ai_medical_devices.csv")
print("\nFirst five FDA device records")
print(data.head())
print("\nOriginal dataset shape:", data.shape)


# 3. Preparing Monthly Time-Series Data
data["final_decision_date"] = pd.to_datetime(data["final_decision_date"], errors="coerce")
data = data.dropna(subset=["final_decision_date"])

# Use the modern AI-device period from 2015 onward.
data = data[data["final_decision_date"] >= "2015-01-01"].copy()
data["Month"] = data["final_decision_date"].dt.to_period("M").dt.to_timestamp()

# Count how many devices received a final decision in every month.
monthly_data = data.groupby("Month").size().rename("Authorization Count").reset_index()

# Reindex so months with zero devices are still present in the sequence.
all_months = pd.date_range(monthly_data["Month"].min(), monthly_data["Month"].max(), freq="MS")
monthly_data = monthly_data.set_index("Month").reindex(all_months, fill_value=0)
monthly_data.index.name = "Month"
monthly_data = monthly_data.reset_index()


# 4. Feature Engineering with Pandas and NumPy
# Sine and cosine preserve the circular relationship between December and January.
monthly_data["Month Number"] = monthly_data["Month"].dt.month
monthly_data["Month Sin"] = np.sin(2 * np.pi * monthly_data["Month Number"] / 12)
monthly_data["Month Cos"] = np.cos(2 * np.pi * monthly_data["Month Number"] / 12)
monthly_data["Rolling Mean 3"] = monthly_data["Authorization Count"].rolling(3, min_periods=1).mean()
monthly_data["Rolling Mean 12"] = monthly_data["Authorization Count"].rolling(12, min_periods=1).mean()

monthly_data.to_csv("outputs/Question_4/monthly_authorization_series.csv", index=False)
monthly_data.describe().T.to_csv("outputs/Question_4/descriptive_statistics.csv")

print("\nMonthly series")
print(monthly_data.head(15))
print("\nNumber of months:", len(monthly_data))


# 5. Exploratory Data Analysis
plt.figure(figsize=(12, 6))
plt.plot(monthly_data["Month"], monthly_data["Authorization Count"],
         marker="o", markersize=3, label="Monthly Count")
plt.plot(monthly_data["Month"], monthly_data["Rolling Mean 12"],
         linewidth=2, label="12-Month Rolling Mean")
plt.title("FDA AI-Enabled Medical Device Authorizations by Month")
plt.xlabel("Month")
plt.ylabel("Authorization Count")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/Question_4/monthly_authorizations.png", dpi=180)
plt.close()


# 6. Scaling and Creating 12-Month Sequences
feature_columns = ["Authorization Count", "Month Sin", "Month Cos", "Rolling Mean 3", "Rolling Mean 12"]
split_index = int(len(monthly_data) * 0.80)

feature_scaler = MinMaxScaler(feature_range=(0, 1))
target_scaler = MinMaxScaler(feature_range=(0, 1))

# Fit only on the training months to avoid future-data leakage.
feature_scaler.fit(monthly_data.loc[:split_index - 1, feature_columns])
target_scaler.fit(monthly_data.loc[:split_index - 1, ["Authorization Count"]])

scaled_features = feature_scaler.transform(monthly_data[feature_columns])
scaled_target = target_scaler.transform(monthly_data[["Authorization Count"]]).flatten()

window_size = 12
X = []
y = []
target_rows = []

for i in range(window_size, len(monthly_data)):
    X.append(scaled_features[i - window_size:i])
    y.append(scaled_target[i])
    target_rows.append(i)

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32)
target_rows = np.array(target_rows)

train_mask = target_rows < split_index
X_train, y_train = X[train_mask], y[train_mask]
X_test, y_test = X[~train_mask], y[~train_mask]
test_rows = target_rows[~train_mask]


# 7. Building RNN, LSTM and GRU Models
def build_model(model_name):
    """Create the selected recurrent architecture using Keras Sequential."""
    model = Sequential()

    if model_name == "SimpleRNN":
        model.add(SimpleRNN(64, return_sequences=True, input_shape=(window_size, len(feature_columns))))
        model.add(Dropout(0.20))
        model.add(SimpleRNN(32))
    elif model_name == "LSTM":
        model.add(LSTM(64, return_sequences=True, input_shape=(window_size, len(feature_columns))))
        model.add(Dropout(0.20))
        model.add(LSTM(32))
    else:
        model.add(GRU(64, return_sequences=True, input_shape=(window_size, len(feature_columns))))
        model.add(Dropout(0.20))
        model.add(GRU(32))

    model.add(Dropout(0.20))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model


# 8. Training and Evaluating the Models
model_names = ["SimpleRNN", "LSTM", "GRU"]
actual_counts = monthly_data.loc[test_rows, "Authorization Count"].to_numpy()
metrics_list = []
predictions = {}

for model_name in model_names:
    print(f"\nTraining {model_name} model")
    model = build_model(model_name)
    early_stop = EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True)

    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=16,
        validation_split=0.15,
        callbacks=[early_stop],
        verbose=1
    )

    scaled_prediction = model.predict(X_test, verbose=0)
    prediction = target_scaler.inverse_transform(scaled_prediction).flatten()
    prediction = np.maximum(prediction, 0)  # Counts cannot be negative.
    predictions[model_name] = prediction

    metrics_list.append({
        "Model": model_name,
        "MAE": mean_absolute_error(actual_counts, prediction),
        "RMSE": np.sqrt(mean_squared_error(actual_counts, prediction)),
        "MAPE Percent": np.mean(np.abs((actual_counts - prediction) / np.maximum(actual_counts, 1))) * 100,
        "R2 Score": r2_score(actual_counts, prediction),
        "Epochs Used": len(history.history["loss"])
    })

    model.save(f"outputs/Question_4/{model_name}_model.keras")


# 9. Seasonal Naive Baseline
# Predict each test month with its value from twelve months earlier.
seasonal_prediction = monthly_data.loc[test_rows - 12, "Authorization Count"].to_numpy()
metrics_list.append({
    "Model": "Seasonal Naive (Previous Year)",
    "MAE": mean_absolute_error(actual_counts, seasonal_prediction),
    "RMSE": np.sqrt(mean_squared_error(actual_counts, seasonal_prediction)),
    "MAPE Percent": np.mean(np.abs((actual_counts - seasonal_prediction) / np.maximum(actual_counts, 1))) * 100,
    "R2 Score": r2_score(actual_counts, seasonal_prediction),
    "Epochs Used": 0
})

metrics_table = pd.DataFrame(metrics_list).sort_values("RMSE")
metrics_table.to_csv("outputs/Question_4/model_metrics.csv", index=False)
print("\nModel comparison")
print(metrics_table)


# 10. Saving and Visualizing Test Predictions
prediction_table = pd.DataFrame({
    "Month": monthly_data.loc[test_rows, "Month"].to_numpy(),
    "Actual Count": actual_counts,
    "Seasonal Naive": seasonal_prediction
})
for model_name in model_names:
    prediction_table[f"Predicted {model_name}"] = predictions[model_name]
prediction_table.to_csv("outputs/Question_4/test_predictions.csv", index=False)

plt.figure(figsize=(12, 6))
plt.plot(prediction_table["Month"], prediction_table["Actual Count"],
         marker="o", label="Actual", color="black")
for model_name in model_names:
    plt.plot(prediction_table["Month"], prediction_table[f"Predicted {model_name}"],
             marker=".", label=model_name)
plt.title("FDA Monthly Authorization Forecast Comparison")
plt.xlabel("Month")
plt.ylabel("Number of Authorizations")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/Question_4/forecast_comparison.png", dpi=180)
plt.close()


# 11. Forecasting the Next Three Months
# Recursive forecasting means every new predicted month becomes part of the
# input window used to predict the following month.
history_frame = monthly_data.copy()
future_rows = []

for step in range(3):
    next_month = history_frame["Month"].max() + pd.offsets.MonthBegin(1)
    last_window = history_frame[feature_columns].tail(window_size)
    scaled_window = feature_scaler.transform(last_window).reshape(
        1, window_size, len(feature_columns)
    )

    model_forecasts = []
    for model_name in model_names:
        saved_model = tf.keras.models.load_model(f"outputs/Question_4/{model_name}_model.keras")
        scaled_forecast = saved_model.predict(scaled_window, verbose=0)
        count_forecast = target_scaler.inverse_transform(scaled_forecast)[0, 0]
        model_forecasts.append(max(float(count_forecast), 0))

    ensemble_count = float(np.mean(model_forecasts))
    future_rows.append([
        next_month, model_forecasts[0], model_forecasts[1],
        model_forecasts[2], ensemble_count, int(round(ensemble_count))
    ])

    # Prepare the predicted month so it can be used in the next recursive step.
    new_row = pd.DataFrame({
        "Month": [next_month],
        "Authorization Count": [ensemble_count],
        "Month Number": [next_month.month],
        "Month Sin": [np.sin(2 * np.pi * next_month.month / 12)],
        "Month Cos": [np.cos(2 * np.pi * next_month.month / 12)],
        "Rolling Mean 3": [pd.concat([
            history_frame["Authorization Count"].tail(2), pd.Series([ensemble_count])
        ]).mean()],
        "Rolling Mean 12": [pd.concat([
            history_frame["Authorization Count"].tail(11), pd.Series([ensemble_count])
        ]).mean()]
    })
    history_frame = pd.concat([history_frame, new_row], ignore_index=True)

future_table = pd.DataFrame(future_rows, columns=[
    "Forecast Month", "SimpleRNN Forecast", "LSTM Forecast", "GRU Forecast",
    "Ensemble Mean", "Rounded Ensemble Count"
])
future_table.to_csv("outputs/Question_4/future_three_month_forecast.csv", index=False)

print("\nNext three-month forecast")
print(future_table)
print("\nQuestion 4 completed - results saved in outputs/Question_4")
