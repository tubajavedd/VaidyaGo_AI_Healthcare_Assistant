from django.urls import path
from .views import register_device

urlpatterns = [
    path("devices/", register_device),
]
