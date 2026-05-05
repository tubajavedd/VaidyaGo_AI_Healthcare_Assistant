from django.urls import path
from .views import register_device,test_notification

urlpatterns = [
    path("devices/", register_device),
    path("test/", test_notification),
]

