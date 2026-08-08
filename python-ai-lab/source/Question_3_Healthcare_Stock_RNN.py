"""
Final assessment - Section B - Question 3

Task aim:
Use Pandas, NumPy, Scikit-learn, TensorFlow and Keras to forecast the next
UnitedHealth Group (UNH) closing price. Compare SimpleRNN, LSTM and GRU models
on the same chronological test data and save their predictions.

The code follows the teacher's Week 17 sequence:
Load -> Prepare -> Scale -> Create Sequences -> Build -> Train -> Predict -> Plot
"""

# 1. Importing Libraries
import warnings
warnings.filterwarnings("ignore")

import os
import re
import random
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
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

os.makedirs("outputs/Question_3", exist_ok=True)


# 2. Loading the Dataset
# The workbook contains ten companies. The UNH sheet is selected for this task.
file_path = "data/stocks/Top 10 Healthcare Companies in the United States.xlsx"
sheet_name = "UnitedHealth Group Inc. (UNH)"
data = pd.read_excel(file_path, sheet_name=sheet_name, header=4)
data.columns = ["Date", "Close", "High", "Low", "Volume"]


# 3. Cleaning and Preparing the Time-Series Data
def convert_date(value):
    """Convert workbook dates such as '2023. 5. 25.' to Pandas datetime."""
    match = re.search(r"(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})", str(value))
    if match:
        year, month, day = map(int, match.groups())
        return pd.Timestamp(year=year, month=month, day=day)
    return pd.NaT


data["Date"] = data["Date"].apply(convert_date)
for column in ["Close", "High", "Low", "Volume"]:
    data[column] = pd.to_numeric(data[column], errors="coerce")

data = data.dropna().sort_values("Date").drop_duplicates("Date").reset_index(drop=True)

# Feature Engineering with Pandas and NumPy.
# Returns and momentum are more stable than directly scaling 23 years of price levels.
data["Log Volume"] = np.log1p(data["Volume"])
data["Daily Return"] = data["Close"].pct_change()
data["Intraday Range"] = (data["High"] - data["Low"]) / data["Close"]
data["Volume Change"] = data["Log Volume"].diff()
data["Momentum 5"] = data["Close"].pct_change(5)
data["Momentum 20"] = data["Close"].pct_change(20)
data = data.dropna().reset_index(drop=True)

print("\nFirst five prepared records")
print(data.head())
print("\nNumber of daily observations:", len(data))
data.describe().T.to_csv("outputs/Question_3/descriptive_statistics.csv")


# 4. Exploratory Data Analysis
plt.figure(figsize=(12, 5))
plt.plot(data["Date"], data["Close"], color="navy")
plt.title("UnitedHealth Group Historical Closing Price")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.tight_layout()
plt.savefig("outputs/Question_3/stock_price_history.png", dpi=180)
plt.close()


# 5. Scaling the Data
feature_columns = ["Daily Return", "Intraday Range", "Volume Change", "Momentum 5", "Momentum 20"]
split_index = int(len(data) * 0.80)

# Scalers are fitted on the training period only to prevent future leakage.
feature_scaler = StandardScaler()
target_scaler = StandardScaler()
feature_scaler.fit(data.loc[:split_index - 1, feature_columns])
target_scaler.fit(data.loc[:split_index - 1, ["Daily Return"]])

scaled_features = feature_scaler.transform(data[feature_columns])
scaled_target = target_scaler.transform(data[["Daily Return"]]).flatten()


# 6. Creating 60-Day Input Sequences
window_size = 60
X = []
y = []
target_rows = []

for i in range(window_size, len(data)):
    X.append(scaled_features[i - window_size:i])
    y.append(scaled_target[i])
    target_rows.append(i)

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32)
target_rows = np.array(target_rows)

# Chronological split: earlier observations train the model; later ones test it.
train_mask = target_rows < split_index
X_train, y_train = X[train_mask], y[train_mask]
X_test, y_test = X[~train_mask], y[~train_mask]
test_rows = target_rows[~train_mask]


# 7. Function for Building RNN, LSTM and GRU Models
def build_model(model_name):
    """Build one recurrent model using the same architecture for fair comparison."""
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


# 8. Training, Predicting and Evaluating All Three Models
model_names = ["SimpleRNN", "LSTM", "GRU"]
metrics_list = []
predictions = {}

actual_close = data.loc[test_rows, "Close"].to_numpy()
previous_close = data.loc[test_rows - 1, "Close"].to_numpy()

for model_name in model_names:
    print(f"\nTraining {model_name} model")
    model = build_model(model_name)

    early_stop = EarlyStopping(
        monitor="val_loss", patience=5, restore_best_weights=True
    )

    history = model.fit(
        X_train, y_train,
        epochs=25,
        batch_size=64,
        validation_split=0.10,
        callbacks=[early_stop],
        verbose=1
    )

    predicted_scaled_return = model.predict(X_test, verbose=0)
    predicted_return = target_scaler.inverse_transform(predicted_scaled_return).flatten()

    # Convert the predicted return back to a real dollar closing price.
    predicted_close = previous_close * (1 + predicted_return)
    predictions[model_name] = predicted_close

    mae = mean_absolute_error(actual_close, predicted_close)
    rmse = np.sqrt(mean_squared_error(actual_close, predicted_close))
    r2 = r2_score(actual_close, predicted_close)
    mape = np.mean(np.abs((actual_close - predicted_close) / actual_close)) * 100
    direction_accuracy = np.mean(
        np.sign(predicted_close - previous_close) == np.sign(actual_close - previous_close)
    )

    metrics_list.append({
        "Model": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE Percent": mape,
        "R2 Score": r2,
        "Directional Accuracy": direction_accuracy,
        "Epochs Used": len(history.history["loss"])
    })

    model.save(f"outputs/Question_3/{model_name}_model.keras")


# 9. Simple Baseline Comparison
# The naive method says tomorrow's close will equal today's close.
metrics_list.append({
    "Model": "Naive Previous Close",
    "MAE": mean_absolute_error(actual_close, previous_close),
    "RMSE": np.sqrt(mean_squared_error(actual_close, previous_close)),
    "MAPE Percent": np.mean(np.abs((actual_close - previous_close) / actual_close)) * 100,
    "R2 Score": r2_score(actual_close, previous_close),
    "Directional Accuracy": 0.0,
    "Epochs Used": 0
})

metrics_table = pd.DataFrame(metrics_list).sort_values("RMSE")
metrics_table.to_csv("outputs/Question_3/model_metrics.csv", index=False)
print("\nModel comparison")
print(metrics_table)


# 10. Saving and Plotting Test Predictions
prediction_table = pd.DataFrame({
    "Date": data.loc[test_rows, "Date"].to_numpy(),
    "Actual Close": actual_close,
    "Previous Close Baseline": previous_close
})
for model_name in model_names:
    prediction_table[f"Predicted {model_name}"] = predictions[model_name]
prediction_table.to_csv("outputs/Question_3/test_predictions.csv", index=False)

plt.figure(figsize=(13, 6))
plt.plot(prediction_table["Date"], prediction_table["Actual Close"], label="Actual", color="black")
for model_name in model_names:
    plt.plot(prediction_table["Date"], prediction_table[f"Predicted {model_name}"],
             label=model_name, alpha=0.8)
plt.title("Actual vs RNN, LSTM and GRU Stock Predictions")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/Question_3/forecast_comparison.png", dpi=180)
plt.close()


# 11. Predicting the Next Trading-Day Closing Price
latest_sequence = scaled_features[-window_size:].reshape(1, window_size, len(feature_columns))
next_predictions = []

for model_name in model_names:
    saved_model = tf.keras.models.load_model(f"outputs/Question_3/{model_name}_model.keras")
    next_scaled_return = saved_model.predict(latest_sequence, verbose=0)
    next_return = target_scaler.inverse_transform(next_scaled_return)[0, 0]
    next_close = data["Close"].iloc[-1] * (1 + next_return)
    next_predictions.append([model_name, next_return, next_close])

next_table = pd.DataFrame(next_predictions, columns=["Model", "Predicted Return", "Predicted Next Close"])
next_table["Ensemble Mean Close"] = next_table["Predicted Next Close"].mean()
next_table.to_csv("outputs/Question_3/next_day_prediction.csv", index=False)

print("\nNext trading-day predictions")
print(next_table)
print("\nQuestion 3 completed - results saved in outputs/Question_3")
print("Educational analysis only - not financial advice.")
