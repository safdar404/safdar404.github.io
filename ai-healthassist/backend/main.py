from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="AI-HealthAssist Clinical Intelligence API", version="0.1.0")

class Symptom(BaseModel):
    code: str
    severity: int = Field(ge=0, le=10)

class Assessment(BaseModel):
    age: int = Field(ge=0, le=120)
    systolic_bp: float | None = None
    diastolic_bp: float | None = None
    bmi: float | None = None
    smoking: bool = False
    symptoms: List[Symptom] = []

@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-healthassist"}

@app.post("/assessment/analyze")
def analyze(data: Assessment):
    """Prototype only. Deterministic safety checks precede any future ML model."""
    codes = {s.code for s in data.symptoms}
    emergency = (
        {"chest_pain", "shortness_of_breath"}.issubset(codes)
        and ({"cold_sweat", "fainting"} & codes)
    ) or {"one_sided_weakness", "speech_difficulty"}.issubset(codes)

    score = 0
    if data.age >= 55: score += 18
    elif data.age >= 45: score += 10
    if data.systolic_bp is not None:
        score += 24 if data.systolic_bp >= 160 else 18 if data.systolic_bp >= 140 else 0
    if data.diastolic_bp is not None:
        score += 10 if data.diastolic_bp >= 100 else 6 if data.diastolic_bp >= 90 else 0
    if data.bmi is not None:
        score += 10 if data.bmi >= 30 else 6 if data.bmi >= 25 else 0
    if data.smoking: score += 14
    if "chest_pain" in codes: score += 16
    if "shortness_of_breath" in codes: score += 10
    score = min(score, 95)

    level = "EMERGENCY" if emergency else "HIGH" if score >= 60 else "MODERATE" if score >= 35 else "LOW"
    return {
        "status": "prototype",
        "triage": level,
        "preliminary_score": score,
        "emergency_rule_triggered": emergency,
        "clinical_review_required": True,
        "model_version": "rules-prototype-0.1",
        "disclaimer": "Synthetic prototype output; not a diagnosis or medical advice."
    }
