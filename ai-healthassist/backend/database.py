"""PostgreSQL/PostGIS-ready persistence layer for AI-HealthAssist."""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_healthassist_demo.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY,
    patient_ref VARCHAR(64) NOT NULL,
    age INTEGER,
    systolic_bp REAL,
    diastolic_bp REAL,
    bmi REAL,
    triage VARCHAR(32),
    preliminary_score REAL,
    emergency_rule_triggered BOOLEAN DEFAULT FALSE,
    model_version VARCHAR(64),
    clinician_decision VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    with engine.begin() as conn:
        conn.execute(text(SCHEMA_SQL))

def save_assessment(result: dict):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO assessments
            (id, patient_ref, triage, preliminary_score,
             emergency_rule_triggered, model_version)
            VALUES (:id, :patient_ref, :triage, :score, :emergency, :model)
        """), {
            "id": result["id"], "patient_ref": result["patient_ref"],
            "triage": result["triage"], "score": result["preliminary_score"],
            "emergency": result["emergency_rule_triggered"],
            "model": result["model_version"]
        })
