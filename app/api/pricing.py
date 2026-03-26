from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.idv_calculator import (
    calculate_idv,
    calculate_repair_cost,
    calculate_claimable
)

router = APIRouter()


class DamageItem(BaseModel):
    part: str
    damage_type: str
    severity: str
    confidence: float


class PricingRequest(BaseModel):
    make: str
    model: str
    year: int
    damages: List[DamageItem]


@router.post("/calculate")
def calculate_claim_price(request: PricingRequest):

    idv_result = calculate_idv(
        request.make,
        request.model,
        request.year
    )

    damage_list = [
        {"part": d.part, "damage_type": d.damage_type}
        for d in request.damages
    ]
    repair_result = calculate_repair_cost(damage_list)

    claim_result = calculate_claimable(
        idv_result["idv"],
        repair_result["total_repair_cost"]
    )

    return {
        "vehicle": f"{request.make} {request.model} {request.year}",
        "idv_calculation": idv_result,
        "repair_calculation": repair_result,
        "claim_summary": claim_result
    }