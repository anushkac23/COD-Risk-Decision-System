import joblib
import pandas as pd
from pathlib import Path


# Locate the trained model
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "cod_risk_model.pkl"


# Load the trained model
model = joblib.load(MODEL_PATH)


def prepare_order_features(order):

    address = str(order.get("address", "")).strip()

    address_incomplete = int(
        address in ["", ".", "None", "nan"]
    )

    pincode = order.get("pincode")

    if pd.isna(pincode):
        pincode = "UNKNOWN"
    else:
        pincode = str(pincode).replace(".0", "")

    features = {
        "order_value": order.get("order_value", 0),
        "num_items": order.get("num_items", 1),
        "customer_prior_orders": order.get(
            "customer_prior_orders", 0
        ),
        "customer_prior_rto": order.get(
            "customer_prior_rto", 0
        ),
        "address_length": len(address),
        "address_incomplete": address_incomplete,
        "city": order.get("city", "UNKNOWN"),
        "state": order.get("state", "UNKNOWN"),
        "pincode": pincode,
        "utm_source": order.get("utm_source", "UNKNOWN"),
        "courier": order.get("courier", "UNKNOWN")
    }

    return pd.DataFrame([features])


def predict_rto_probability(order):

    input_data = prepare_order_features(order)

    probabilities = model.predict_proba(input_data)

    # RTO is represented by class 1
    rto_probability = probabilities[0][
        list(model.classes_).index(1)
    ]

    return round(float(rto_probability), 4)