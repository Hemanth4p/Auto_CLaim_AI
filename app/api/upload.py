from fastapi import APIRouter, UploadFile, File
from typing import List
import os
import uuid
from datetime import datetime

from app.utils.exif import extract_exif
from app.services.fraud_detection import check_fraud

router = APIRouter()

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/")
async def upload_images(
    files: List[UploadFile] = File(...),
    incident_date: str = "2026-03-20"
):
    claim_id = str(uuid.uuid4())[:8].upper()
    results = []

    for file in files:
        contents = await file.read()
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        exif = extract_exif(file_path)
        fraud, reason = check_fraud(exif, incident_date)

        results.append({
            "file": file.filename,
            "fraud": fraud,
            "reason": reason,
            "confidence_score": None
        })

    overall_fraud = any(r["fraud"] for r in results)

    return {
        "claim_id": claim_id,
        "incident_date": incident_date,
        "submitted_at": datetime.now().isoformat(),
        "overall_fraud_flag": overall_fraud,
        "status": "FLAGGED FOR REVIEW" if overall_fraud else "PASSED FRAUD CHECK",
        "results": results
    }