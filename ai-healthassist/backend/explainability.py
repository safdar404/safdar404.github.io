"""Lightweight, model-agnostic explanation layer for the research prototype.
This is a directional attribution demo, not validated SHAP or clinical advice.
"""
FEATURE_LABELS={"age":"Age","systolic_bp":"Systolic blood pressure","bmi":"BMI","smoking":"Smoking history"}
def explain(age,systolic_bp,bmi,smoking):
    values={"age":max(0,min(1,(age-40)/40)),"systolic_bp":max(0,min(1,(systolic_bp-120)/80)),"bmi":max(0,min(1,(bmi-25)/15)),"smoking":1 if smoking else 0}
    weights={"age":.30,"systolic_bp":.38,"bmi":.17,"smoking":.15}
    ranked=sorted(((k,values[k]*weights[k]) for k in values),key=lambda x:x[1],reverse=True)
    return {"method":"directional-feature-attribution","factors":[{"feature":FEATURE_LABELS[k],"contribution":round(v,3),"direction":"increases risk" if v>0 else "neutral"} for k,v in ranked],"validated":False}
