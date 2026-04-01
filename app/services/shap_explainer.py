import shap
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

PLOTS_DIR = "data/shap_plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def build_sample_model():
    """
    Train a simple Randomforest model on sample insurance data.
    On Colab day this gets replaced with real trained model.
    """
    data = {
        "vehicle_age": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        "damage_severity": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
        "num_damages": [1, 2, 1, 3, 2, 1, 2, 3, 1, 2],
        "is_comprehensive": [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        "has_zero_dep": [1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        "repair_cost": [
            8000, 18000, 5000, 32000, 22000,
            6000, 14000, 28000, 9000, 16000
        ]
    }

    df = pd.DataFrame(data)
    X = df.drop("repair_cost", axis=1)
    y = df["repair_cost"]

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)

    return model, list(X.columns)


def generate_shap_explanation(
    vehicle_age: int,
    damages: list,
    policy_type: str,
    has_zero_dep: bool,
    idv: float,
    repair_cost: float,
    claim_id: str
) -> dict:
    """
    Generate SHAP explanation for the claim amount.
    Returns explanation text and plot path.
    """

    model, feature_names = build_sample_model()

    severity_map = {"low": 1, "medium": 2, "high": 3}
    avg_severity = np.mean([
        severity_map.get(d.get("severity", "medium"), 2)
        for d in damages
    ]) if damages else 2

    is_comprehensive = 1 if "comprehensive" in policy_type.lower() else 0
    zero_dep = 1 if has_zero_dep else 0

    input_data = pd.DataFrame([{
        "vehicle_age": vehicle_age,
        "damage_severity": avg_severity,
        "num_damages": len(damages),
        "is_comprehensive": is_comprehensive,
        "has_zero_dep": zero_dep
    }])

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_data)

    feature_impacts = {}
    for i, feature in enumerate(feature_names):
        feature_impacts[feature] = round(float(shap_values[0][i]), 2)

    plot_path = os.path.join(PLOTS_DIR, f"shap_{claim_id}.png")
    plt.figure(figsize=(8, 4))
    colors = [
        "#E24B4A" if v < 0 else "#1D9E75"
        for v in feature_impacts.values()
    ]
    plt.barh(
        list(feature_impacts.keys()),
        list(feature_impacts.values()),
        color=colors
    )
    plt.xlabel("Impact on Repair Cost (Rs)")
    plt.title(f"SHAP Explanation — Claim {claim_id}")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=100, bbox_inches="tight")
    plt.close()

    explanations = []

    if feature_impacts.get("vehicle_age", 0) > 0:
        explanations.append(
            f"Vehicle age ({vehicle_age} years) increases repair cost "
            f"by Rs {abs(feature_impacts['vehicle_age']):.0f}"
        )
    else:
        explanations.append(
            f"Vehicle age ({vehicle_age} years) reduces repair cost "
            f"by Rs {abs(feature_impacts['vehicle_age']):.0f}"
        )

    if feature_impacts.get("damage_severity", 0) > 0:
        explanations.append(
            f"High damage severity increases cost "
            f"by Rs {abs(feature_impacts['damage_severity']):.0f}"
        )

    if feature_impacts.get("num_damages", 0) > 0:
        explanations.append(
            f"{len(damages)} damages found increases total cost "
            f"by Rs {abs(feature_impacts['num_damages']):.0f}"
        )

    if zero_dep:
        explanations.append(
            "Zero Depreciation add-on active — "
            "full part cost claimable without depreciation deduction"
        )

    deductible = 1000
    claimable = round(min(repair_cost, idv) - deductible)

    return {
        "shap_values": feature_impacts,
        "explanations": explanations,
        "plot_path": plot_path,
        "base_repair_cost": repair_cost,
        "idv": idv,
        "deductible": deductible,
        "final_claimable": claimable
    }