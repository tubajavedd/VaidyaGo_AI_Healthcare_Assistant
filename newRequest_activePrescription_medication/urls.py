from django.urls import path
from .views import *

urlpatterns = [
<<<<<<< HEAD
    path("medications/", MedicationListView.as_view()),
    path("pharmacies/", PharmacyListView.as_view()),

    path("prescription-request/add/", CreatePrescriptionRequestView.as_view()),
    path("prescription-request/", PatientPrescriptionListView.as_view()),
=======
    path('medications/', MedicationListView.as_view()),
    path('pharmacies/', PharmacyListView.as_view()),
    path('requests/create/', CreatePrescriptionRequestView.as_view()),
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
]