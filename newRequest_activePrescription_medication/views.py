from rest_framework import generics, permissions
from .models import Medication, Pharmacy, PrescriptionRequest
from .serializers import *


# 🔽 Dropdown: Medications
class MedicationListView(generics.ListAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


# 🔽 Dropdown: Pharmacies
class PharmacyListView(generics.ListAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


# 🔽 Create New Request
class CreatePrescriptionRequestView(generics.CreateAPIView):
    serializer_class = PrescriptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


# 🔽 List Patient Requests
class PatientPrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrescriptionRequest.objects.filter(
            patient=self.request.user
        ).order_by("-created_at")