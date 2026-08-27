"""FastAPI-friendly ML inference wrapper using the synthetic experiment.
Research prototype only; not for diagnosis or treatment."""
from ml_engine import train_and_evaluate
_model = None
_metrics = None

def get_model():
    global _model, _metrics
    if _model is None:
        _model, _metrics = train_and_evaluate()
    return _model, _metrics

def predict(age: int, systolic_bp: float, bmi: float, smoking: bool):
    model, metrics = get_model()
    probability = float(model.predict_proba([[age, systolic_bp, bmi, int(smoking)]])[0, 1])
    risk_class = "HIGH" if probability >= .67 else "MODERATE" if probability >= .34 else "LOW"
    return {"risk_probability": round(probability, 4), "risk_class": risk_class,
            "model_version": metrics["model_version"], "clinical_review_required": True,
            "clinical_validation": False}
