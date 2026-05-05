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
    """
    queryset = DoctorPersonalInfo.objects.filter(status='approved').select_related('professional_info')
    serializer_class = DoctorListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

