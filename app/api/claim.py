from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import os
import shutil
import uuid
from datetime import datetime

from app.utils.exif import extract_exif
from app.services.fraud_detection import check_fraud
from app.services.vehicle_identification import identify_vehicle
from app.services.damage_detection import detect_damage
from app.services.idv_calculator import (
    calculate_idv, calculate_repair_cost, calculate_claimable
)
from app.services.rag_engine import check_coverage
from app.services.shap_explainer import generate_shap_explanation
from app.services.report_generator import generate_pdf_report
from app.services.schedule_parser import parse_schedule

router = APIRouter()

UPLOAD_FOLDER = "data/uploads"
POLICY_FOLDER = "data/policies"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(POLICY_FOLDER, exist_ok=True)


@router.post("/process")
async def process_claim(
    files: List[UploadFile] = File(...),
    policy_schedule: UploadFile = File(...),
    incident_date: str = Form(default="2026-04-03")
):
    claim_id = str(uuid.uuid4())[:8].upper()
    submitted_at = datetime.now().isoformat()

    saved_paths = []
    fraud_results = []

    for file in files:
        contents = await file.read()
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(contents)
        saved_paths.append(file_path)

        exif = extract_exif(file_path)
        fraud, reason = check_fraud(exif, incident_date)
        fraud_results.append({
            "file": file.filename,
            "fraud": fraud,
            "reason": reason
        })

    overall_fraud = any(r["fraud"] for r in fraud_results)

    if overall_fraud:
        return {
            "claim_id": claim_id,
            "submitted_at": submitted_at,
            "status": "FLAGGED FOR REVIEW",
            "fraud_flag": True,
            "fraud_details": fraud_results,
            "message": "Claim flagged due to suspicious photo metadata."
        }

    schedule_path = os.path.join(POLICY_FOLDER, policy_schedule.filename)
    schedule_contents = await policy_schedule.read()
    with open(schedule_path, "wb") as f:
        f.write(schedule_contents)

    schedule_data = parse_schedule(schedule_path)

    vehicle_result = identify_vehicle(saved_paths[0])

    damage_result = detect_damage(saved_paths)
    damages = damage_result["damages"]

    vehicle_age = 2026 - int(vehicle_result.get("year", 2021))
    idv_result = calculate_idv(
        vehicle_result.get("make", "Tata"),
        vehicle_result.get("model", "Nexon"),
        int(vehicle_result.get("year", 2021))
    )

    if schedule_data["idv"] > 0:
        idv_value = schedule_data["idv"]
    else:
        idv_value = idv_result["idv"]

    repair_result = calculate_repair_cost(damages)
    claim_result = calculate_claimable(
        idv_value,
        repair_result["total_repair_cost"]
    )

    policy_wording_path = f"data/policies/policy_wording_bajaj.pdf"
    if os.path.exists(policy_wording_path):
        coverage_result = check_coverage(policy_wording_path, damages)
    else:
        coverage_result = {
            "policy_type": schedule_data["policy_type"],
            "coverage_details": [
                {**d, "covered": True,
                 "reason": "Covered under accidental damage"}
                for d in damages
            ]
        }

    covered_damages = [
        d for d in coverage_result["coverage_details"]
        if d.get("covered", True)
    ]

    covered_repair = calculate_repair_cost(covered_damages)
    final_claim = calculate_claimable(
        idv_value,
        covered_repair["total_repair_cost"]
    )

    shap_result = generate_shap_explanation(
        vehicle_age=vehicle_age,
        damages=damages,
        policy_type=schedule_data["policy_type"],
        has_zero_dep=schedule_data["has_zero_dep"],
        idv=idv_value,
        repair_cost=covered_repair["total_repair_cost"],
        claim_id=claim_id
    )

    pdf_path = generate_pdf_report(
        claim_id=claim_id,
        vehicle_make=vehicle_result.get("make", "Tata"),
        vehicle_model=vehicle_result.get("model", "Nexon"),
        vehicle_year=int(vehicle_result.get("year", 2021)),
        damages=coverage_result["coverage_details"],
        policy_type=schedule_data["policy_type"],
        shap_result=shap_result
    )

    return {
        "claim_id": claim_id,
        "submitted_at": submitted_at,
        "status": "CLAIM REPORT GENERATED",
        "fraud_check": "PASSED",
        "vehicle": {
            "make": vehicle_result.get("make"),
            "model": vehicle_result.get("model"),
            "year": vehicle_result.get("year"),
            "confidence": vehicle_result.get("confidence")
        },
        "schedule_data": schedule_data,
        "damages_detected": len(damages),
        "damages_covered": len(covered_damages),
        "idv": idv_value,
        "total_repair_cost": covered_repair["total_repair_cost"],
        "final_claimable": shap_result["final_claimable"],
        "deductible": 1000,
        "shap_explanations": shap_result["explanations"],
        "pdf_report": pdf_path,
        "coverage_details": coverage_result["coverage_details"]
    }