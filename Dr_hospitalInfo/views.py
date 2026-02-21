from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import get_object_or_404

from .models import DoctorHospitalInfo
from .serializers import DoctorHospitalInfoSerializer
from Dr_personalInfo.models import DoctorPersonalInfo


class DoctorHospitalInfoCreateView(generics.CreateAPIView):
    serializer_class = DoctorHospitalInfoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        doctor_id = self.kwargs.get('doctor_id')
        doctor = get_object_or_404(DoctorPersonalInfo, id=doctor_id)
        serializer.save(doctor=doctor)


class DoctorHospitalInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorHospitalInfoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return DoctorHospitalInfo.objects.filter(doctor_id=doctor_id)
