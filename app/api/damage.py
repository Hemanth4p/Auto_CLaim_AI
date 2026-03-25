from fastapi import APIRouter, UploadFile, File
from typing import List
import os
import shutil

from app.services.damage_detection import detect_damage

router = APIRouter()

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/detect")
async def detect_damage_api(
    files: List[UploadFile] = File(...)
):
    saved_paths = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)

    result = detect_damage(saved_paths)

    return {
        "photos_received": len(saved_paths),
        "filenames": [f.filename for f in files],
        "damage_report": result
    }