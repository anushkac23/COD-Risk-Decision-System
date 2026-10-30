print("Decision engine test started!")
from services.decision_engine import evaluate_order


# Sample COD order
sample_order = {
    "order_id": "TEST001",
    "order_value": 649,
    "num_items": 2,
    "customer_prior_orders": 3,
    "customer_prior_rto": 1,
    "address": "Flat 202, Sector 15, New Panvel",
    "pincode": "410206"
}


# Test different RTO probabilities
test_probabilities = [
    0.10,
    0.22,
    0.40,
    0.65
]


print("\n========== DECISION ENGINE TEST ==========")

for probability in test_probabilities:

    result = evaluate_order(
        sample_order,
        probability
    )

    print("\nOrder ID:", result["order_id"])
    print("RTO Probability:", result["risk_probability"], "%")
    print("Risk Level:", result["risk_level"])
    print("Recommended Action:", result["recommended_action"])
    print("Reasons:")

    for reason in result["reasons"]:
        print("-", reason)

print("\n========== TEST COMPLETED ==========")