from rest_framework import serializers
from .models import DoctorPersonalInfo

class DoctorPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPersonalInfo
        fields = '__all__'
