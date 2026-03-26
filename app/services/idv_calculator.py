MARKET_PRICES = {
    "tata nexon": 900000,
    "maruti swift": 650000,
    "hyundai creta": 1100000,
    "mahindra xuv700": 1400000,
    "honda city": 1200000,
    "tata altroz": 750000,
    "maruti baleno": 700000,
    "hyundai i20": 800000,
}

DEPRECIATION_RATES = {
    0: 0.05,
    1: 0.15,
    2: 0.20,
    3: 0.30,
    4: 0.40,
    5: 0.50,
}

REPAIR_COSTS = {
    "front_bumper": {"dent": 8000, "scratch": 3000,
                     "shatter": 14000, "crack": 6000},
    "left_headlight": {"shatter": 18000, "crack": 5000,
                       "scratch": 2000, "dent": 4000},
    "right_headlight": {"shatter": 18000, "crack": 5000,
                        "scratch": 2000, "dent": 4000},
    "door_panel": {"dent": 6000, "scratch": 4000,
                   "shatter": 10000, "crack": 5000},
    "rear_bumper": {"dent": 7000, "scratch": 3000,
                    "shatter": 12000, "crack": 5000},
    "windshield": {"shatter": 15000, "crack": 8000,
                   "scratch": 3000, "dent": 2000},
    "bonnet": {"dent": 9000, "scratch": 4000,
               "shatter": 20000, "crack": 7000},
}

COMPULSORY_DEDUCTIBLE = 1000


def calculate_idv(make: str, model: str, year: int) -> dict:
    current_year = 2026
    age = current_year - year

    car_key = f"{make} {model}".lower()
    market_price = MARKET_PRICES.get(car_key, 800000)

    age_key = min(age, 5)
    depreciation = DEPRECIATION_RATES.get(age_key, 0.50)

    idv = market_price * (1 - depreciation)

    return {
        "market_price": market_price,
        "vehicle_age_years": age,
        "depreciation_percent": depreciation * 100,
        "idv": round(idv)
    }


def calculate_repair_cost(damages: list) -> dict:
    total = 0
    breakdown = []

    for damage in damages:
        part = damage.get("part", "")
        damage_type = damage.get("damage_type", "")

        part_costs = REPAIR_COSTS.get(part, {})
        cost = part_costs.get(damage_type, 5000)

        breakdown.append({
            "part": part,
            "damage_type": damage_type,
            "repair_cost": cost
        })
        total += cost

    return {
        "total_repair_cost": total,
        "breakdown": breakdown
    }


def calculate_claimable(idv: float, repair_cost: float) -> dict:
    covered = min(repair_cost, idv)
    claimable = covered - COMPULSORY_DEDUCTIBLE

    return {
        "repair_cost": repair_cost,
        "idv": round(idv),
        "covered_amount": round(covered),
        "compulsory_deductible": COMPULSORY_DEDUCTIBLE,
        "claimable_amount": round(claimable)
    }