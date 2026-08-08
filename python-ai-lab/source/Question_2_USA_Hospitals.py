"""
Final assessment - Section A - Question 2

Task aim:
Use the USA Hospitals dataset with NumPy, Pandas, Seaborn and Scikit-learn.
The program performs:
1. Data cleaning, descriptive statistics and EDA
2. Regression to predict hospital bed capacity
3. Classification to predict whether a hospital has a helipad
4. Ensemble learning for classification and regression
5. K-Means clustering to group similar hospitals
"""

# 1. Importing Libraries
import warnings
warnings.filterwarnings("ignore")

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestRegressor, GradientBoostingRegressor, VotingRegressor,
    RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
)
from sklearn.cluster import KMeans
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, silhouette_score
)

np.random.seed(42)
sns.set_style("whitegrid")

# Always use the folder containing this Python file as the working folder.
# This prevents FileNotFoundError when VS Code starts the script elsewhere.
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

os.makedirs("outputs/Question_2", exist_ok=True)


# 2. Loading and Understanding the Dataset
data = pd.read_csv("data/hospitals/Hospitals.csv", encoding="utf-8-sig")
print("\nFirst five hospital records")
print(data.head())
print("\nDataset shape:", data.shape)
print("\nColumn names")
print(data.columns.tolist())


# 3. Data Cleaning
# OBJECTID uniquely identifies hospitals; duplicate IDs are removed.
data = data.drop_duplicates(subset=["OBJECTID"]).reset_index(drop=True)

# The dataset uses -999 to represent unavailable numeric values.
data = data.replace([-999, "-999"], np.nan)

numeric_columns = ["BEDS", "LATITUDE", "LONGITUDE", "TTL_STAFF"]
for column in numeric_columns:
    data[column] = pd.to_numeric(data[column], errors="coerce")

# Create a binary target: Y=1 means a helipad is available.
data["HELIPAD_TARGET"] = data["HELIPAD"].astype(str).str.upper().map({"Y": 1, "N": 0})

print("\nMissing values in important columns")
print(data[numeric_columns + ["HELIPAD_TARGET"]].isnull().sum())

data[numeric_columns].describe().T.to_csv("outputs/Question_2/descriptive_statistics.csv")


# 4. Exploratory Data Analysis
plt.figure(figsize=(9, 5))
sns.histplot(data=data, x="BEDS", bins=50, kde=True, color="steelblue")
plt.xlim(0, data["BEDS"].quantile(0.99))
plt.title("Distribution of Hospital Beds")
plt.tight_layout()
plt.savefig("outputs/Question_2/bed_distribution.png", dpi=180)
plt.close()

top_types = data["TYPE"].value_counts().head(8).index
plt.figure(figsize=(10, 5))
sns.countplot(data=data[data["TYPE"].isin(top_types)], y="TYPE",
              order=top_types, palette="viridis")
plt.title("Main Hospital Types")
plt.tight_layout()
plt.savefig("outputs/Question_2/hospital_types.png", dpi=180)
plt.close()


# 5. Regression Task - Predict the Number of Beds
# POPULATION is deliberately excluded because it frequently copies BEDS and
# would cause target leakage (the answer would already be inside the features).
regression_features = [
    "TYPE", "STATUS", "STATE", "OWNER", "TRAUMA", "HELIPAD", "VAL_METHOD",
    "LATITUDE", "LONGITUDE", "TTL_STAFF", "ST_FIPS"
]
regression_data = data[data["BEDS"].gt(0)].copy()
# A few extremely large facilities dominate RMSE, so the highest 0.5% are
# treated as outliers for this general hospital-capacity model.
bed_upper_limit = regression_data["BEDS"].quantile(0.995)
regression_data = regression_data[regression_data["BEDS"].le(bed_upper_limit)]
X = regression_data[regression_features]
y = regression_data["BEDS"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

numeric_features = ["LATITUDE", "LONGITUDE", "TTL_STAFF", "ST_FIPS"]
categorical_features = ["TYPE", "STATUS", "STATE", "OWNER", "TRAUMA", "HELIPAD", "VAL_METHOD"]

# ColumnTransformer performs median filling/scaling for numeric columns and
# most-frequent filling/one-hot encoding for categorical columns.
preprocessor = ColumnTransformer([
    ("numeric", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), numeric_features),
    ("categorical", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical_features)
])

regression_models = {
    "Random Forest": RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}

regression_results = []
fitted_regressors = {}
for model_name, model in regression_models.items():
    model_pipeline = Pipeline([("preprocessing", preprocessor), ("model", model)])
    model_pipeline.fit(X_train, y_train)
    prediction = model_pipeline.predict(X_test)
    fitted_regressors[model_name] = model_pipeline
    regression_results.append({
        "Model": model_name,
        "MAE": mean_absolute_error(y_test, prediction),
        "RMSE": np.sqrt(mean_squared_error(y_test, prediction)),
        "R2 Score": r2_score(y_test, prediction)
    })

# VotingRegressor averages Random Forest and Gradient Boosting predictions.
voting_regressor = VotingRegressor([
    ("random_forest", RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)),
    ("gradient_boosting", GradientBoostingRegressor(random_state=42))
])
voting_pipeline = Pipeline([("preprocessing", preprocessor), ("model", voting_regressor)])
voting_pipeline.fit(X_train, y_train)
voting_prediction = voting_pipeline.predict(X_test)

regression_results.append({
    "Model": "Voting Regressor",
    "MAE": mean_absolute_error(y_test, voting_prediction),
    "RMSE": np.sqrt(mean_squared_error(y_test, voting_prediction)),
    "R2 Score": r2_score(y_test, voting_prediction)
})

pd.DataFrame({"Actual Beds": y_test, "Predicted Beds": voting_prediction}).to_csv(
    "outputs/Question_2/bed_predictions.csv", index=False
)
regression_results = pd.DataFrame(regression_results).sort_values("RMSE")
regression_results.to_csv("outputs/Question_2/bed_regression_results.csv", index=False)
print("\nBed regression results")
print(regression_results)


# 6. Classification Task - Predict Helipad Availability
classification_features = ["TYPE", "STATUS", "STATE", "OWNER", "BEDS", "LATITUDE", "LONGITUDE"]
classification_data = data.dropna(subset=["HELIPAD_TARGET"]).copy()
Xc = classification_data[classification_features]
yc = classification_data["HELIPAD_TARGET"].astype(int)

Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    Xc, yc, test_size=0.20, random_state=42, stratify=yc
)

class_numeric = ["BEDS", "LATITUDE", "LONGITUDE"]
class_categorical = ["TYPE", "STATUS", "STATE", "OWNER"]
class_preprocessor = ColumnTransformer([
    ("numeric", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), class_numeric),
    ("categorical", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]), class_categorical)
])

classification_models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

classification_results = []
for model_name, model in classification_models.items():
    model_pipeline = Pipeline([("preprocessing", class_preprocessor), ("model", model)])
    model_pipeline.fit(Xc_train, yc_train)
    prediction = model_pipeline.predict(Xc_test)
    probability = model_pipeline.predict_proba(Xc_test)[:, 1]
    classification_results.append({
        "Model": model_name,
        "Accuracy": accuracy_score(yc_test, prediction),
        "Precision": precision_score(yc_test, prediction),
        "Recall": recall_score(yc_test, prediction),
        "F1 Score": f1_score(yc_test, prediction),
        "ROC AUC": roc_auc_score(yc_test, probability)
    })

voting_classifier = VotingClassifier([
    ("logistic", LogisticRegression(max_iter=2000, random_state=42)),
    ("random_forest", RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)),
    ("gradient_boosting", GradientBoostingClassifier(random_state=42))
], voting="soft")

voting_class_pipeline = Pipeline([
    ("preprocessing", class_preprocessor),
    ("model", voting_classifier)
])
voting_class_pipeline.fit(Xc_train, yc_train)
helipad_prediction = voting_class_pipeline.predict(Xc_test)
helipad_probability = voting_class_pipeline.predict_proba(Xc_test)[:, 1]

classification_results.append({
    "Model": "Soft Voting Classifier",
    "Accuracy": accuracy_score(yc_test, helipad_prediction),
    "Precision": precision_score(yc_test, helipad_prediction),
    "Recall": recall_score(yc_test, helipad_prediction),
    "F1 Score": f1_score(yc_test, helipad_prediction),
    "ROC AUC": roc_auc_score(yc_test, helipad_probability)
})

classification_results = pd.DataFrame(classification_results).sort_values("ROC AUC", ascending=False)
classification_results.to_csv("outputs/Question_2/helipad_classification_results.csv", index=False)
print("\nHelipad classification results")
print(classification_results)
print("\nSoft voting classification report")
print(classification_report(yc_test, helipad_prediction))


# 7. K-Means Clustering of Hospitals
cluster_data = data[["BEDS", "LATITUDE", "LONGITUDE", "TTL_STAFF"]].copy()
cluster_values = SimpleImputer(strategy="median").fit_transform(cluster_data)
cluster_values = StandardScaler().fit_transform(cluster_values)

scores = []
for k in range(2, 8):
    test_model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = test_model.fit_predict(cluster_values)
    scores.append([k, silhouette_score(cluster_values, labels)])

score_table = pd.DataFrame(scores, columns=["K", "Silhouette Score"])
best_k = int(score_table.loc[score_table["Silhouette Score"].idxmax(), "K"])
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
data["Hospital Cluster"] = kmeans.fit_predict(cluster_values)

data[["NAME", "STATE", "TYPE", "BEDS", "LATITUDE", "LONGITUDE", "Hospital Cluster"]].to_csv(
    "outputs/Question_2/hospital_clusters.csv", index=False
)
score_table.to_csv("outputs/Question_2/cluster_selection.csv", index=False)

plt.figure(figsize=(11, 6))
sns.scatterplot(data=data, x="LONGITUDE", y="LATITUDE", hue="Hospital Cluster",
                palette="tab10", s=20, alpha=0.7)
plt.title(f"USA Hospital Clusters (K={best_k})")
plt.tight_layout()
plt.savefig("outputs/Question_2/hospital_clusters.png", dpi=180)
plt.close()

print("\nBest number of hospital clusters:", best_k)
print("\nQuestion 2 completed - results saved in outputs/Question_2")
