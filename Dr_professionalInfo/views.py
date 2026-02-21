from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import get_object_or_404

from .models import DoctorProfessionalInfo
from .serializers import DoctorProfessionalInfoSerializer
from Dr_personalInfo.models import DoctorPersonalInfo


class DoctorProfessionalInfoCreateView(generics.CreateAPIView):
    serializer_class = DoctorProfessionalInfoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        doctor_id = self.kwargs.get('doctor_id')
        doctor = get_object_or_404(DoctorPersonalInfo, id=doctor_id)
        serializer.save(doctor=doctor)


class DoctorProfessionalInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorProfessionalInfoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get_object(self):
        doctor_id = self.kwargs.get('doctor_id')
        return get_object_or_404(
            DoctorProfessionalInfo,
            doctor_id=doctor_id
        )
