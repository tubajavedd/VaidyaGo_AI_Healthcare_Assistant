from django.urls import path
from .views import DoctorSlotListCreateAPI, DoctorSlotDetailAPI

urlpatterns = [
    path('doctor-slots/', DoctorSlotListCreateAPI.as_view()),
    path('doctor-slots/<int:pk>/', DoctorSlotDetailAPI.as_view()),
]
