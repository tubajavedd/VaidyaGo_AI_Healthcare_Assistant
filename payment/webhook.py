import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import hmac
import hashlib

from .models import Payment


@csrf_exempt
def webhook_handler(request):
    body = request.body
    signature = request.headers.get('X-Razorpay-Signature')

    expected_signature = hmac.new(
        bytes(settings.RAZORPAY_WEBHOOK_SECRET, 'utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        return JsonResponse({"error": "Invalid signature"}, status=400)

    data = json.loads(body)

    if data['event'] == 'payment.captured':
        payment_entity = data['payload']['payment']['entity']

        try:
            payment = Payment.objects.get(order_id=payment_entity['order_id'])
            payment.payment_id = payment_entity['id']
            payment.status = "paid"
            payment.save()
        except Payment.DoesNotExist:
            pass

    return JsonResponse({"status": "ok"})