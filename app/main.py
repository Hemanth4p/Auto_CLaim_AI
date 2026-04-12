from fastapi import FastAPI
from app.api import upload
from app.api import damage
from app.api import pricing
from app.api import policy
from app.api import report
from app.api import claim

app = FastAPI(
    title="AutoClaim AI",
    description="Intelligent Vehicle Insurance Claim Engine",
    version="1.0.0"
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(damage.router, prefix="/damage", tags=["Damage"])
app.include_router(pricing.router, prefix="/pricing", tags=["Pricing"])
app.include_router(policy.router, prefix="/policy", tags=["Policy"])
app.include_router(report.router, prefix="/report", tags=["Report"])
app.include_router(claim.router, prefix="/claim", tags=["Claim"])

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "AutoClaim AI",
        "developer": "Hemanth4p",
        "layers_complete": [
            "upload",
            "fraud_detection",
            "vehicle_identification",
            "damage_detection",
            "idv_pricing",
            "rag_policy_engine",
            "shap_report",
            "full_pipeline"
        ]
    }