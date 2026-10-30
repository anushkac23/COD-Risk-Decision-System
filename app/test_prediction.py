from services.prediction_service import predict_rto_probability


# Sample COD order
sample_order = {
    "order_id": "TEST001",
    "order_value": 649,
    "num_items": 2,
    "customer_prior_orders": 0,
    "customer_prior_rto": 0,
    "address": "Flat 202, Sector 15, New Panvel",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "410206",
    "utm_source": "instagram_organic",
    "courier": "Delhivery"
}


# Predict RTO probability
probability = predict_rto_probability(sample_order)

print("\n========== COD RISK PREDICTION ==========")
print("Order ID:", sample_order["order_id"])
print("RTO Probability:", probability * 100, "%")
print("=========================================")