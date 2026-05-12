from django.urls import path
from .views import register_device, test_notification, list_notifications

urlpatterns = [
    path("devices/", register_device),
    path("test/", test_notification),
    path("list/", list_notifications),
]
