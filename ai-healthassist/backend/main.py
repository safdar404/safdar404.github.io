from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from database import init_db, engine
from sqlalchemy import text

app = FastAPI(title="AI-HealthAssist Clinical Intelligence API", version="0.2.0")

class Symptom(BaseModel):
    code: str
    severity: int = Field(ge=0, le=10)

class Assessment(BaseModel):
    patient_ref: str = "DEMO-PATIENT"
    age: int = Field(ge=0, le=120)
    systolic_bp: float | None = None
    diastolic_bp: float | None = None
    bmi: float | None = None
    smoking: bool = False
    symptoms: List[Symptom] = []

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-healthassist", "version": "0.2.0"}

@app.post("/assessment/analyze")
def analyze(data: Assessment):
    codes = {s.code for s in data.symptoms}
    emergency = (
        {"chest_pain", "shortness_of_breath"}.issubset(codes)
        and ({"cold_sweat", "fainting"} & codes)
    ) or {"one_sided_weakness", "speech_difficulty"}.issubset(codes)
    score = 0
    if data.age >= 55: score += 18
    elif data.age >= 45: score += 10
    if data.systolic_bp is not None: score += 24 if data.systolic_bp >= 160 else 18 if data.systolic_bp >= 140 else 0
    if data.diastolic_bp is not None: score += 10 if data.diastolic_bp >= 100 else 6 if data.diastolic_bp >= 90 else 0
    if data.bmi is not None: score += 10 if data.bmi >= 30 else 6 if data.bmi >= 25 else 0
    if data.smoking: score += 14
    if "chest_pain" in codes: score += 16
    if "shortness_of_breath" in codes: score += 10
    score = min(score, 95)
    level = "EMERGENCY" if emergency else "HIGH" if score >= 60 else "MODERATE" if score >= 35 else "LOW"
    with engine.begin() as conn:
        next_id = conn.execute(text("SELECT COALESCE(MAX(id),0)+1 FROM assessments")).scalar_one()
        conn.execute(text("""INSERT INTO assessments
            (id, patient_ref, age, systolic_bp, diastolic_bp, bmi, triage,
             preliminary_score, emergency_rule_triggered, model_version)
            VALUES (:id,:patient_ref,:age,:sbp,:dbp,:bmi,:triage,:score,:emergency,:model)"""),
            {"id":next_id,"patient_ref":data.patient_ref,"age":data.age,"sbp":data.systolic_bp,
             "dbp":data.diastolic_bp,"bmi":data.bmi,"triage":level,"score":score,
             "emergency":emergency,"model":"rules-prototype-0.2"})
    return {"status":"prototype","assessment_id":next_id,"patient_ref":data.patient_ref,
            "triage":level,"preliminary_score":score,"emergency_rule_triggered":emergency,
            "clinical_review_required":True,"model_version":"rules-prototype-0.2",
            "disclaimer":"Synthetic prototype output; not a diagnosis or medical advice."}

@app.get("/assessments")
def assessments():
    with engine.begin() as conn:
        rows = conn.execute(text("""SELECT id,patient_ref,triage,preliminary_score,
            emergency_rule_triggered,model_version,created_at FROM assessments ORDER BY id DESC LIMIT 100""")).mappings().all()
    return {"count": len(rows), "items": [dict(r) for r in rows]}

@app.post("/assessments/{assessment_id}/decision")
def clinician_decision(assessment_id: int, decision: str):
    allowed = {"AGREED", "MODIFIED", "REJECTED"}
    if decision.upper() not in allowed: raise HTTPException(400, "Decision must be AGREED, MODIFIED, or REJECTED")
    with engine.begin() as conn:
        result = conn.execute(text("UPDATE assessments SET clinician_decision=:d WHERE id=:id"), {"d":decision.upper(),"id":assessment_id})
        if result.rowcount == 0: raise HTTPException(404, "Assessment not found")
    return {"assessment_id":assessment_id,"clinician_decision":decision.upper(),"audit_event":"recorded"}
