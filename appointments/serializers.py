from rest_framework import serializers
from .models import Appointment
from Dr_personalInfo.models import DoctorPersonalInfo

from DoctorSlot.serializers import TimeSlotSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorPersonalInfo.objects.all(), required=False)
    doctor_name = serializers.SerializerMethodField()
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    slot_details = TimeSlotSerializer(source='slot', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'doctor_name', 'slot', 'slot_details', 'user', 
            'patient_name', 'patient_phone', 'patient_email',
            'patient_age', 'patient_gender', 'patient_mrn',
            'appointment_type', 'location',
            'start_time', 'end_time', 'status', 
            'reschedule_reason', 'rejection_reason', 'created_at'
        ]

    def get_doctor_name(self, obj):
        if obj.doctor:
            return f"{obj.doctor.first_name} {obj.doctor.last_name}"
        return "Unknown Doctor"