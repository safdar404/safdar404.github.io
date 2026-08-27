"""Transparent synthetic ML experiment for AI-HealthAssist.
This is a research demo, not a validated clinical model."""
from pathlib import Path
import json
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

FEATURES = ["age", "systolic_bp", "bmi", "smoking"]
MODEL_VERSION = "CVD-Synthetic-HGB-0.1"
ARTIFACT = Path(__file__).with_name("cvd_model_metrics.json")

def build_synthetic_dataset(n=1600, seed=42):
    rng = np.random.default_rng(seed)
    age = rng.integers(25, 81, n)
    sbp = np.clip(rng.normal(128 + (age - 45) * .35, 18, n), 90, 210)
    bmi = np.clip(rng.normal(26, 4.5, n), 16, 45)
    smoking = rng.binomial(1, .22, n)
    logit = -5.0 + .035*age + .025*sbp + .07*bmi + .75*smoking
    p = 1/(1+np.exp(-logit))
    y = rng.binomial(1, p)
    return np.column_stack([age, sbp, bmi, smoking]), y

def train_and_evaluate():
    X, y = build_synthetic_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, stratify=y, random_state=42)
    model = HistGradientBoostingClassifier(max_iter=120, learning_rate=.08, random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= .5).astype(int)
    metrics = {
        "model_version": MODEL_VERSION, "dataset": "synthetic", "n_samples": int(len(y)),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
        "clinical_validation": False, "status": "research_prototype"
    }
    ARTIFACT.write_text(json.dumps(metrics, indent=2))
    return model, metrics

if __name__ == "__main__":
    _, metrics = train_and_evaluate()
    print(json.dumps(metrics, indent=2))
