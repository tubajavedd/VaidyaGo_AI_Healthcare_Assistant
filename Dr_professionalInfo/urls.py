from django.urls import path
from .views import (
    DoctorProfessionalInfoCreateView,
    DoctorProfessionalInfoDetailView
)

urlpatterns = [
    path(
        'doctor/<int:doctor_id>/professional-info/',
        DoctorProfessionalInfoCreateView.as_view(),
        name='doctor-professional-create'
    ),

    path(
        'doctor/<int:doctor_id>/professional-info/<int:pk>/',
        DoctorProfessionalInfoDetailView.as_view(),
        name='doctor-professional-detail'
    ),
]
