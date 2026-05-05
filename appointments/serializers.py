from rest_framework import serializers
from .models import Appointment
from Dr_personalInfo.models import DoctorPersonalInfo
from rest_framework import serializers

from DoctorSlot.serializers import TimeSlotSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorPersonalInfo.objects.all(), required=False)
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    slot_details = TimeSlotSerializer(source='slot', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'slot', 'slot_details', 'user', 
            'patient_name', 'patient_phone', 'patient_email',
            'patient_age', 'patient_mrn',
            'appointment_type', 'location',
            'start_time', 'end_time', 'status', 
            'reschedule_reason', 'rejection_reason', 'created_at'
        ]