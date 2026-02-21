from django.urls import path
from .views import (
    DoctorDocumentCreateView,
    DoctorDocumentListView,
    DoctorDocumentDetailView
)

urlpatterns = [
    path(
        'doctor/<int:doctor_id>/documents/',
        DoctorDocumentCreateView.as_view(),
        name='doctor-document-create'
    ),

    path(
        'doctor/<int:doctor_id>/documents/list/',
        DoctorDocumentListView.as_view(),
        name='doctor-document-list'
    ),

    path(
        'doctor/<int:doctor_id>/documents/<int:pk>/',
        DoctorDocumentDetailView.as_view(),
        name='doctor-document-detail'
    ),
]
