from rest_framework import serializers
from .models import DoctorProfessionalInfo


class DoctorProfessionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfessionalInfo
        fields = [
            'id',
            'doctor_employee_id',
            'department',
            'specialization',
            'qualification',
            'years_of_experience',
            'medical_license_number',
            'medical_council',
            'created_at'
        ]

        read_only_fields = ['id', 'created_at']
