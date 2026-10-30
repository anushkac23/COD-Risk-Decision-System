import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "config" / "risk_config.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_risk_level(risk_probability):

    config = load_config()
    thresholds = config["risk_thresholds"]

    # Convert decimal probability into percentage
    risk_percentage = risk_probability * 100

    if risk_percentage < thresholds["low"]:
        return "LOW"

    elif risk_percentage < thresholds["medium"]:
        return "MEDIUM"

    elif risk_percentage < thresholds["high"]:
        return "HIGH"

    else:
        return "VERY HIGH"


def recommend_action(risk_level):

    config = load_config()
    actions = config["decision_rules"]

    action_mapping = {
        "LOW": actions["low"],
        "MEDIUM": actions["medium"],
        "HIGH": actions["high"],
        "VERY HIGH": actions["very_high"]
    }

    return action_mapping.get(
        risk_level, "HOLD_FOR_REVIEW"
    )
    


def generate_reasons(order):

    reasons = []

    prior_rto = order.get("customer_prior_rto", 0)

    try:
        prior_rto = int(prior_rto)
    except (ValueError, TypeError):
        prior_rto = 0

    address = str(order.get("address", "")).strip()

    pincode = order.get("pincode")
    pincode_missing = (
        pincode is None or
        str(pincode).strip().lower() in ["", "nan", "none"]
    )

    if prior_rto >= 2:
        reasons.append(
            f"Customer has {prior_rto} previous RTO orders."
        )

    elif prior_rto == 1:
        reasons.append(
            "Customer has one previous RTO order."
        )

    if address.lower() in ["", ".", "none", "nan"]:
        reasons.append(
            "Address information appears incomplete."
        )

    if pincode_missing:
        reasons.append(
            "Pincode information is missing."
        )

    if not reasons:
        reasons.append(
            "No major historical customer or address warning was identified."
        )

    return reasons

def evaluate_order(order, risk_probability):

    risk_level = calculate_risk_level(risk_probability)

    action = recommend_action(risk_level)

    reasons = generate_reasons(order)

    # Avoid automatically holding a first-time customer
    if (
        order.get("customer_prior_orders", 0) == 0
        and action == "HOLD_FOR_REVIEW"
    ):
        action = "WHATSAPP_CONFIRMATION"

    return {
        "order_id": order.get("order_id"),
        "risk_probability": round(
            risk_probability * 100, 2
        ),
        "risk_level": risk_level,
        "recommended_action": action,
        "reasons": reasons
    }