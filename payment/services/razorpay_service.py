import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))


def create_order(amount):
    order_data = {
        "amount": amount * 100,  # paise
        "currency": "INR",
        "payment_capture": 1
    }
    return client.order.create(order_data)


def verify_signature(data):
    try:
        client.utility.verify_payment_signature(data)
        return True
    except:
        return False


def refund_payment(payment_id, amount=None):
    return client.payment.refund(payment_id, {
        "amount": amount * 100 if amount else None
    })