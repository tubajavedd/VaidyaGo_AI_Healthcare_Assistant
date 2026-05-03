from django.urls import path
from .views import *

urlpatterns = [
    path("medications/", MedicationListView.as_view()),
    path("pharmacies/", PharmacyListView.as_view()),

    path("prescription-request/add/", CreatePrescriptionRequestView.as_view()),
    path("prescription-request/", PatientPrescriptionListView.as_view()),
]