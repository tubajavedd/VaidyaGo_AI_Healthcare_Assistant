from rest_framework import generics, permissions
from .models import Medication, Pharmacy, PrescriptionRequest
from .serializers import *

# GET + POST medications
class MedicationListView(generics.ListCreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


# GET + POST pharmacies
class PharmacyListView(generics.ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


# Submit request
class CreatePrescriptionRequestView(generics.CreateAPIView):
    serializer_class = PrescriptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)