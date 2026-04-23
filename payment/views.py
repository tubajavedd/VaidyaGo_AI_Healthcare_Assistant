import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from .services.razorpay_service import create_order, refund_payment


@csrf_exempt
def create_order_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = data.get("amount")
        user_id = data.get("user_id")

        order = create_order(amount)

        payment = Payment.objects.create(
            user_id=user_id,
            order_id=order['id'],
            amount=amount
        )

        return JsonResponse(order)


@csrf_exempt
def refund_view(request, payment_id):
    if request.method == "POST":
        payment = Payment.objects.get(payment_id=payment_id)

        refund_payment(payment.payment_id)

        payment.status = "refunded"
        payment.save()

        return JsonResponse({"status": "refunded"})
    

    #history



    from django.core.paginator import Paginator


def payment_history(request):
    user_id = request.GET.get("user_id")

    payments = Payment.objects.filter(user_id=user_id).order_by('-created_at')

    paginator = Paginator(payments, 10)
    page = request.GET.get('page')

    data = paginator.get_page(page)

    result = list(data.object_list.values())

    return JsonResponse({
        "data": result,
        "total_pages": paginator.num_pages
    })