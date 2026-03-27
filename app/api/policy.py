# from fastapi import APIRouter, UploadFile, File, Form
# from typing import List
# import os
# import shutil
# import json

# from app.services.rag_engine import check_coverage

# router = APIRouter()

# POLICY_FOLDER = "data/policies"
# os.makedirs(POLICY_FOLDER, exist_ok=True)


# @router.post("/check")
# async def check_policy_coverage(
#     policy_pdf: UploadFile = File(...),
#     damages: str = Form(...)
# ):
#     pdf_path = os.path.join(POLICY_FOLDER, policy_pdf.filename)
#     with open(pdf_path, "wb") as buffer:
#         shutil.copyfileobj(policy_pdf.file, buffer)

#     damages_list = json.loads(damages)

#     result = check_coverage(pdf_path, damages_list)

#     return {
#         "pdf_received": policy_pdf.filename,
#         "coverage_result": result
#     }



from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import os
import shutil
import json

from app.services.rag_engine import check_coverage

router = APIRouter()

POLICY_FOLDER = "data/policies"


@router.post("/check")
async def check_policy_coverage(
    policy_pdf: UploadFile = File(...),
    damages: str = Form(...)
):
    os.makedirs(POLICY_FOLDER, exist_ok=True)

    pdf_path = os.path.join(POLICY_FOLDER, policy_pdf.filename)
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(policy_pdf.file, buffer)

    damages_list = json.loads(damages)

    result = check_coverage(pdf_path, damages_list)

    return {
        "pdf_received": policy_pdf.filename,
        "coverage_result": result
    }
