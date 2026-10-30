from datetime import datetime, timedelta


def generate_confirmation_message(order):
    return (
        f"Hello {order.get('customer_name', 'Customer')}! 👋\n\n"
        f"Thank you for ordering from us.\n"
        f"Your order ID is {order.get('order_id')}.\n"
        f"Order amount: ₹{order.get('order_value')}.\n\n"
        "Please confirm your COD order by replying YES or NO.\n\n"
        "If we don't receive your response within 24 hours, "
        "your order will be kept on hold."
    )


def generate_prepaid_message(order, discount_percent=5):

    order_value = float(order.get("order_value", 0))

    discount = round(
        order_value * discount_percent / 100, 2
    )

    final_amount = round(order_value - discount, 2)

    return (
        f"Hello {order.get('customer_name', 'Customer')}!\n\n"
        f"You can save ₹{discount} on your order "
        f"by choosing prepaid payment.\n\n"
        f"Original amount: ₹{order_value}\n"
        f"Discount: ₹{discount}\n"
        f"Prepaid amount: ₹{final_amount}\n\n"
        "Would you like to switch to prepaid payment?"
    )


def process_customer_response(response):

    response = response.strip().upper()

    if response in ["YES", "Y", "CONFIRM"]:
        return {
            "status": "CONFIRMED",
            "message": "Thank you! Your order has been confirmed."
        }

    elif response in ["NO", "N", "CANCEL"]:
        return {
            "status": "CANCELLED",
            "message": "Your order cancellation request has been received."
        }

    elif response in ["PREPAID", "PAY"]:
        return {
            "status": "PREPAID_REQUESTED",
            "message": "We will share the prepaid payment instructions."
        }

    else:
        return {
            "status": "NEEDS_CLARIFICATION",
            "message": "Please reply YES to confirm or NO to cancel your order."
        }


def check_response_timeout(sent_time):

    current_time = datetime.now()

    deadline = sent_time + timedelta(hours=24)

    if current_time >= deadline:
        return {
            "status": "TIMEOUT",
            "message": (
                "No response received within 24 hours. "
                "Order has been placed on hold for manual review."
            )
        }

    return {
        "status": "WAITING",
        "message": "Waiting for customer response."
    }