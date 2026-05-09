from django.urls import path
from .views import (
    DoctorPersonalInfoCreateView,
    DoctorPersonalInfoDetailView,
    ApprovedDoctorListView,
    DoctorSubmitView,
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
    path(
        'approved-doctors/',
        ApprovedDoctorListView.as_view(),
        name='approved_doctor_list'
    ),
    path(
        'submit/<int:pk>/',
        DoctorSubmitView.as_view(),
        name='doctor_submit'
    ),
]
