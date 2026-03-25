from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.vehicle_identification import identify_vehicle

router = APIRouter()

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/identify")
async def identify_vehicle_api(
    file: UploadFile = File(...)
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = identify_vehicle(file_path)

    return {
        "filename": file.filename,
        "vehicle": result
    }