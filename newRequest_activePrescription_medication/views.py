from rest_framework import generics, permissions
from .models import Medication, Pharmacy, PrescriptionRequest
from .serializers import *


from datetime import timedelta
from django.utils import timezone
from prescription_management.models import PrescribedMedicine


# 🔽 Dropdown: Medications (Filtered by "About to End")
class MedicationListView(generics.ListAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()
        seven_days_from_now = today + timedelta(days=7)
        
        prescribed_meds = PrescribedMedicine.objects.filter(prescription__patient=user)
        
        expiring_names = []
        self.expiring_data = {}  # Store days_left mapping
        
        for pm in prescribed_meds:
            p_date = pm.prescription.prescription_date or pm.prescription.created_at.date()
            if pm.duration_days:
                end_date = p_date + timedelta(days=pm.duration_days)
                days_left = (end_date - today).days
                
                # Filter: expiring within 7 days
                if 0 <= days_left <= 7:
                    expiring_names.append(pm.name)
                    self.expiring_data[pm.name] = days_left
        
        return Medication.objects.filter(name__in=expiring_names)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['expiring_data'] = getattr(self, 'expiring_data', {})
        return context


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
