from django.urls import path
from .views import (
    DoctorHospitalInfoCreateView,
    DoctorHospitalInfoDetailView
)

urlpatterns = [
    path(
        'doctor/<int:doctor_id>/hospital-info/',
        DoctorHospitalInfoCreateView.as_view(),
        name='doctor-hospital-create'
    ),

    path(
        'doctor/<int:doctor_id>/hospital-info/<int:pk>/',
        DoctorHospitalInfoDetailView.as_view(),
        name='doctor-hospital-detail'
    ),
]
