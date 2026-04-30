from rest_framework import generics, permissions
from .models import PastMedication, Doctor
from .serializers import PastMedicationSerializer, DoctorSerializer

#create past medication entry for patient
class CreatePastMedicationView(generics.CreateAPIView):
    serializer_class = PastMedicationSerializer
    permission_classes = [permissions.IsAuthenticated]


#list view of patient history of past medications
class PatientPastMedicationListView(generics.ListAPIView):
    serializer_class = PastMedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PastMedication.objects.filter(patient=self.request.user).order_by("-created_at")
    
    
#doctor list view for dropdown in frontend 
class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer