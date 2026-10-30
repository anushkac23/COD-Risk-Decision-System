from datetime import datetime, timedelta

from services.whatsapp_service import (
    generate_confirmation_message,
    generate_prepaid_message,
    process_customer_response,
    check_response_timeout
)


# Sample COD order
sample_order = {
    "order_id": "TEST001",
    "customer_name": "Anushka",
    "order_value": 649
}


print("\n========== WHATSAPP AUTOMATION TEST ==========")


# 1. Confirmation message
print("\n1. CONFIRMATION MESSAGE")
print(generate_confirmation_message(sample_order))


# 2. Prepaid discount message
print("\n2. PREPAID DISCOUNT MESSAGE")
print(generate_prepaid_message(sample_order))


# 3. Customer responses
print("\n3. CUSTOMER RESPONSE TESTS")

responses = ["YES", "NO", "Hello", "PREPAID"]

for response in responses:
    result = process_customer_response(response)

    print("\nCustomer:", response)
    print("Status:", result["status"])
    print("Message:", result["message"])


# 4. Response timeout
print("\n4. 24-HOUR TIMEOUT TEST")

sent_time = datetime.now() - timedelta(hours=25)

result = check_response_timeout(sent_time)

print("Status:", result["status"])
print("Message:", result["message"])


print("\n========== TEST COMPLETED ==========")