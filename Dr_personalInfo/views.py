from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from .models import DoctorPersonalInfo
from .serializers import DoctorPersonalInfoSerializer, DoctorListSerializer


class DoctorPersonalInfoCreateView(generics.CreateAPIView):
    queryset = DoctorPersonalInfo.objects.all()
    serializer_class = DoctorPersonalInfoSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]


class DoctorPersonalInfoDetailView(generics.RetrieveUpdateAPIView):
    queryset = DoctorPersonalInfo.objects.all()
    serializer_class = DoctorPersonalInfoSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]


class ApprovedDoctorListView(generics.ListAPIView):
    """
    API to fetch all registered doctors who are approved by the admin.
    Supports filtering via query parameters:
    - ?department=...
    - ?specialization=...
    """
    serializer_class = DoctorListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = DoctorPersonalInfo.objects.filter(status='approved').select_related('professional_info')
        
        department = self.request.query_params.get('department')
        specialization = self.request.query_params.get('specialization')

        if department:
            queryset = queryset.filter(professional_info__department__iexact=department)
        
        if specialization:
            queryset = queryset.filter(professional_info__specialization__iexact=specialization)
            
        return queryset

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class DoctorSubmitView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, pk):
        doctor = get_object_or_404(DoctorPersonalInfo, pk=pk)
        
        # Change status from incomplete to pending
        if doctor.status == 'incomplete':
            doctor.status = 'pending'
            doctor.save()
            return Response({"message": "Profile submitted successfully and is under admin review."}, status=status.HTTP_200_OK)
        elif doctor.status == 'rejected':
            doctor.status = 'pending'
            doctor.save()
            return Response({"message": "Profile re-submitted successfully and is under admin review."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"Profile already in {doctor.status} status."}, status=status.HTTP_400_BAD_REQUEST)


