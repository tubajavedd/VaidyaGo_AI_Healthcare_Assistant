from django.urls import path
from .views import *

urlpatterns = [
    path("past-medications/", PatientPastMedicationListView.as_view()),
    path("past-medications/add/", CreatePastMedicationView.as_view()),
    path("doctors/", DoctorListView.as_view()),
]