from django.urls import path
from .views import (
    DoctorPersonalInfoCreateView,
    DoctorPersonalInfoDetailView,
)

urlpatterns = [
    path(
        'doctor-personal-info/',
        DoctorPersonalInfoCreateView.as_view(),
        name='doctor_personal_info'
    ),
    path(
        'doctor-personal-info/<int:pk>/',
        DoctorPersonalInfoDetailView.as_view(),
        name='doctor_personal_info_update'
    ),
]
