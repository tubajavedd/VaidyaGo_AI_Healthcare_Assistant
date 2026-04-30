from django.urls import path
from .views import *

urlpatterns = [
    path('medications/', MedicationListView.as_view()),
    path('pharmacies/', PharmacyListView.as_view()),
    path('requests/create/', CreatePrescriptionRequestView.as_view()),
]