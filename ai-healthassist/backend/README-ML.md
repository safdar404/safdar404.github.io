# AI-HealthAssist ML Engine

This module is a **synthetic research prototype**. It is not clinically validated and must not be used for diagnosis or treatment.

## Run

```bash
pip install numpy scikit-learn
python ml_engine.py
```

The script generates a deterministic synthetic dataset, trains a histogram gradient-boosting classifier, evaluates ROC-AUC, accuracy, precision and recall, and writes `cvd_model_metrics.json`.

## Production gate

Before any clinical use: replace synthetic data with governed clinical data, define the target and cohort prospectively, prevent leakage, perform temporal/external validation, calibration and subgroup analysis, document intended use, monitor drift, and obtain appropriate clinical/regulatory review.
