from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import get_object_or_404

from .models import DoctorDocument
from .serializers import DoctorDocumentSerializer
from Dr_personalInfo.models import DoctorPersonalInfo

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def final_submit(request, doctor_id):
    doctor = get_object_or_404(DoctorPersonalInfo, id=doctor_id)

    # check documents uploaded
    docs = DoctorDocument.objects.filter(doctor=doctor)

    if not docs.exists():
        return Response({
            "error": "Please upload documents first"
        }, status=400)

<<<<<<< HEAD
    # MAIN LOGIC
=======
    # 🔥 MAIN LOGIC
>>>>>>> 0430290e280f82c69137655a897b42e4079297d1
    doctor.status = 'pending'
    doctor.save()

    return Response({
        "message": "Profile submitted successfully. Waiting for admin approval."
    })

class DoctorDocumentCreateView(generics.CreateAPIView):
    serializer_class = DoctorDocumentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        doctor_id = self.kwargs.get('doctor_id')
        doctor = get_object_or_404(DoctorPersonalInfo, id=doctor_id)
        serializer.save(doctor=doctor)


class DoctorDocumentListView(generics.ListAPIView):
    serializer_class = DoctorDocumentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return DoctorDocument.objects.filter(doctor_id=doctor_id)


class DoctorDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorDocumentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return DoctorDocument.objects.filter(doctor_id=doctor_id)
