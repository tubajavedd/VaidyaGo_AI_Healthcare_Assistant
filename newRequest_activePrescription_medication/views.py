from rest_framework import generics, permissions
from .models import Medication, Pharmacy, PrescriptionRequest
from .serializers import *

<<<<<<< HEAD

# 🔽 Dropdown: Medications
class MedicationListView(generics.ListAPIView):
=======
# GET + POST medications
class MedicationListView(generics.ListCreateAPIView):
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


<<<<<<< HEAD
# 🔽 Dropdown: Pharmacies
class PharmacyListView(generics.ListAPIView):
=======
# GET + POST pharmacies
class PharmacyListView(generics.ListCreateAPIView):
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


<<<<<<< HEAD
# 🔽 Create New Request
=======
# Submit request
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
class CreatePrescriptionRequestView(generics.CreateAPIView):
    serializer_class = PrescriptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

<<<<<<< HEAD

# 🔽 List Patient Requests
class PatientPrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrescriptionRequest.objects.filter(
            patient=self.request.user
        ).order_by("-created_at")
=======
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
