from django.urls import path
from .views import create_order_view, refund_view
from .webhook import webhook_handler

urlpatterns = [
    path('create-order/', create_order_view),
    path('webhook/', webhook_handler),
    path('<str:payment_id>/refund', refund_view),
]