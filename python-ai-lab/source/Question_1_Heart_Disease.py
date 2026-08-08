"""
Final assessment - Section A - Question 1

Task aim:
Use NumPy, Pandas, Seaborn and Scikit-learn on the UCI Heart Disease dataset.
The program performs:
1. Data cleaning and descriptive statistics
2. Exploratory Data Analysis (EDA)
3. Classification of heart disease
4. Ensemble learning with VotingClassifier
5. Regression to predict maximum heart rate (thalach)
6. K-Means clustering to discover patient groups

This code follows the numbered, step-by-step style used in the teacher's
Week 8 and Week 11 examples.
"""

# 1. Importing the required libraries
import warnings
warnings.filterwarnings("ignore")

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, VotingClassifier,
    RandomForestRegressor, GradientBoostingRegressor
)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score,
    silhouette_score
)

np.random.seed(42)
sns.set_style("whitegrid")

# Always use the folder containing this Python file as the working folder.
# This prevents FileNotFoundError when VS Code starts the script elsewhere.
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

os.makedirs("outputs/Question_1", exist_ok=True)


# 2. Loading the dataset with Pandas
data = pd.read_csv("data/heart/heart_disease_combined.csv")

print("\nFirst five rows")
print(data.head())
print("\nDataset shape:", data.shape)
print("\nColumn information")
print(data.info())


# 3. Data cleaning
# Remove exact duplicate records so one patient row is not counted twice.
data = data.drop_duplicates().reset_index(drop=True)

# Convert the source place into numeric dummy columns.
data = pd.get_dummies(data, columns=["source"], drop_first=True, dtype=int)

# Show missing values before imputation.
print("\nMissing values")
print(data.isnull().sum())

# Save descriptive statistics required in the question paper.
data.describe().T.to_csv("outputs/Question_1/descriptive_statistics.csv")
print("\nDescriptive statistics")
print(data.describe().T)


# 4. Exploratory Data Analysis using Seaborn and Matplotlib
plt.figure(figsize=(6, 4))
sns.countplot(data=data, x="target", palette="Set2")
plt.title("Heart Disease Target Distribution")
plt.xlabel("Target: 0 = No Disease, 1 = Disease")
plt.tight_layout()
plt.savefig("outputs/Question_1/target_distribution.png", dpi=180)
plt.close()

plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(numeric_only=True), cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("outputs/Question_1/correlation_heatmap.png", dpi=180)
plt.close()


# 5. Selecting classification features and target
# X contains independent variables and y contains the dependent target.
X = data.drop(columns=["target"])
y = data["target"].astype(int)

# Split before fitting the imputer/scaler to prevent test-data leakage.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Fill missing values with the training median.
imputer = SimpleImputer(strategy="median")
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Standardization is important for Logistic Regression and SVM.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)


# 6. Classification model development and prediction
classification_models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=42),
    "Support Vector Machine": SVC(probability=True, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

classification_results = []
trained_models = {}

for model_name, model in classification_models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    y_probability = model.predict_proba(X_test_scaled)[:, 1]
    trained_models[model_name] = model

    classification_results.append({
        "Model": model_name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC AUC": roc_auc_score(y_test, y_probability)
    })


# 7. Ensemble Learning - Soft Voting Classifier
# Soft voting averages the probabilities of different classifiers.
voting_model = VotingClassifier(
    estimators=[
        ("logistic", LogisticRegression(max_iter=2000, random_state=42)),
        ("random_forest", RandomForestClassifier(n_estimators=200, random_state=42)),
        ("gradient_boosting", GradientBoostingClassifier(random_state=42))
    ],
    voting="soft"
)
voting_model.fit(X_train_scaled, y_train)
voting_pred = voting_model.predict(X_test_scaled)
voting_probability = voting_model.predict_proba(X_test_scaled)[:, 1]

classification_results.append({
    "Model": "Soft Voting Ensemble",
    "Accuracy": accuracy_score(y_test, voting_pred),
    "Precision": precision_score(y_test, voting_pred),
    "Recall": recall_score(y_test, voting_pred),
    "F1 Score": f1_score(y_test, voting_pred),
    "ROC AUC": roc_auc_score(y_test, voting_probability)
})

classification_results = pd.DataFrame(classification_results).sort_values(
    "ROC AUC", ascending=False
)
classification_results.to_csv("outputs/Question_1/classification_results.csv", index=False)

print("\nClassification results")
print(classification_results)
print("\nVoting classifier report")
print(classification_report(y_test, voting_pred))

# Confusion Matrix visualization in the same style as the teacher's example.
cm = confusion_matrix(y_test, voting_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Confusion Matrix - Voting Classifier")
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.tight_layout()
plt.savefig("outputs/Question_1/confusion_matrix.png", dpi=180)
plt.close()


# 8. Regression Task - predict maximum heart rate (thalach)
regression_data = data.dropna(subset=["thalach"]).copy()
X_reg = regression_data.drop(columns=["thalach", "target"])
y_reg = regression_data["thalach"]

Xr_train, Xr_test, yr_train, yr_test = train_test_split(
    X_reg, y_reg, test_size=0.20, random_state=42
)

reg_imputer = SimpleImputer(strategy="median")
Xr_train = reg_imputer.fit_transform(Xr_train)
Xr_test = reg_imputer.transform(Xr_test)

regression_models = {
    "Random Forest Regressor": RandomForestRegressor(n_estimators=200, random_state=42),
    "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42)
}

regression_results = []
for model_name, model in regression_models.items():
    model.fit(Xr_train, yr_train)
    prediction = model.predict(Xr_test)
    regression_results.append({
        "Model": model_name,
        "MAE": mean_absolute_error(yr_test, prediction),
        "RMSE": np.sqrt(mean_squared_error(yr_test, prediction)),
        "R2 Score": r2_score(yr_test, prediction)
    })

regression_results = pd.DataFrame(regression_results).sort_values("RMSE")
regression_results.to_csv("outputs/Question_1/regression_results.csv", index=False)
print("\nRegression results")
print(regression_results)


# 9. Unsupervised Learning - K-Means Clustering
cluster_features = data.drop(columns=["target"])
cluster_values = SimpleImputer(strategy="median").fit_transform(cluster_features)
cluster_values = StandardScaler().fit_transform(cluster_values)

# Test different values of K and select the highest silhouette score.
silhouette_results = []
for k in range(2, 7):
    test_kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = test_kmeans.fit_predict(cluster_values)
    silhouette_results.append([k, silhouette_score(cluster_values, labels)])

silhouette_table = pd.DataFrame(silhouette_results, columns=["K", "Silhouette Score"])
best_k = int(silhouette_table.loc[silhouette_table["Silhouette Score"].idxmax(), "K"])

kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
data["Patient Cluster"] = kmeans.fit_predict(cluster_values)
data.to_csv("outputs/Question_1/patient_clusters.csv", index=False)
silhouette_table.to_csv("outputs/Question_1/cluster_selection.csv", index=False)

# PCA changes many columns into two components only for visualization.
pca = PCA(n_components=2)
pca_values = pca.fit_transform(cluster_values)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=pca_values[:, 0], y=pca_values[:, 1],
                hue=data["Patient Cluster"], palette="tab10")
plt.title(f"Patient Clusters using K-Means (K={best_k})")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.tight_layout()
plt.savefig("outputs/Question_1/patient_clusters.png", dpi=180)
plt.close()

print("\nBest number of patient clusters:", best_k)
print("\nQuestion 1 completed - results saved in outputs/Question_1")
