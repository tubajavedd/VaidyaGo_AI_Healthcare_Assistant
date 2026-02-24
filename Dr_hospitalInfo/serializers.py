from rest_framework import serializers
from .models import DoctorHospitalInfo


class DoctorHospitalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorHospitalInfo
        fields = [
            'id',
            'joining_date',
            'employment_type',
            'consultation_fees',
            'leave_day',
            'created_at'
        ]

        read_only_fields = ['id', 'created_at']
