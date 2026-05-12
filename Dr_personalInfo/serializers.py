from rest_framework import serializers
from .models import DoctorPersonalInfo

class DoctorPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPersonalInfo
        fields = '__all__'


class DoctorListSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source='professional_info.specialization', read_only=True)
    department = serializers.CharField(source='professional_info.department', read_only=True)
    years_of_experience = serializers.IntegerField(source='professional_info.years_of_experience', read_only=True)

    class Meta:
        model = DoctorPersonalInfo
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'mobile_number', 
            'specialization', 
            'department', 
            'years_of_experience',
            'city', 
            'status'
        ]
