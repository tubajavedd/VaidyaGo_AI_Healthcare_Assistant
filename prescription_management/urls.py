from django.urls import path
from .views import (
    PrescriptionUploadView,
    PrescriptionListView,
    ActivePrescriptionView,
    DashboardSummaryView
)

urlpatterns = [
    path('prescriptions/upload/', PrescriptionUploadView.as_view(), name='prescription-upload'),
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/active/', ActivePrescriptionView.as_view(), name='prescription-active'),
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]
