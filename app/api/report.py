from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os

from app.services.shap_explainer import generate_shap_explanation
from app.services.report_generator import generate_pdf_report

router = APIRouter()


class DamageItem(BaseModel):
    part: str
    damage_type: str
    cause: str = "accident"
    severity: str = "high"
    confidence: float = 90.0
    covered: bool = True
    reason: str = ""


class ReportRequest(BaseModel):
    claim_id: str
    vehicle_make: str
    vehicle_model: str
    vehicle_year: int
    damages: List[DamageItem]
    policy_type: str = "Comprehensive"
    has_zero_dep: bool = False
    idv: float = 500000
    repair_cost: float = 26000


@router.post("/generate")
def generate_claim_report(request: ReportRequest):

    vehicle_age = 2026 - request.vehicle_year

    shap_result = generate_shap_explanation(
        vehicle_age=vehicle_age,
        damages=[d.dict() for d in request.damages],
        policy_type=request.policy_type,
        has_zero_dep=request.has_zero_dep,
        idv=request.idv,
        repair_cost=request.repair_cost,
        claim_id=request.claim_id
    )

    pdf_path = generate_pdf_report(
        claim_id=request.claim_id,
        vehicle_make=request.vehicle_make,
        vehicle_model=request.vehicle_model,
        vehicle_year=request.vehicle_year,
        damages=[d.dict() for d in request.damages],
        policy_type=request.policy_type,
        shap_result=shap_result
    )

    return {
        "claim_id": request.claim_id,
        "vehicle": f"{request.vehicle_make} {request.vehicle_model} {request.vehicle_year}",
        "policy_type": request.policy_type,
        "total_damages": len(request.damages),
        "covered_damages": sum(1 for d in request.damages if d.covered),
        "repair_cost": request.repair_cost,
        "idv": request.idv,
        "final_claimable": shap_result["final_claimable"],
        "deductible": shap_result["deductible"],
        "shap_explanations": shap_result["explanations"],
        "shap_values": shap_result["shap_values"],
        "pdf_report": pdf_path,
        "status": "CLAIM REPORT GENERATED"
    }


@router.get("/download/{claim_id}")
def download_report(claim_id: str):
    pdf_path = f"data/reports/claim_{claim_id}.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"AutoClaim_{claim_id}.pdf"
        )
    return {"error": "Report not found"}