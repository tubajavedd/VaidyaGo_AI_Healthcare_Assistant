from rest_framework import serializers
from .models import Appointment
from Dr_personalInfo.models import DoctorPersonalInfo

from DoctorSlot.serializers import TimeSlotSerializer

# 📋 Doctor Serializer for appointment views
class DoctorDetailSerializer(serializers.ModelSerializer):
    """Detailed doctor information for patient appointment views"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DoctorPersonalInfo
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'mobile_number', 'alternate_number', 'email',
            'city', 'address', 'gender'
        ]
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


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
            'patient_weight', 'patient_disease', 'patient_heart_rate', 
            'patient_blood_type', 'patient_photo',
            'appointment_type', 'location',
            'start_time', 'end_time', 'status', 
            'reschedule_reason', 'rejection_reason', 'created_at'
        ]

    def get_doctor_name(self, obj):
        if obj.doctor:
            return f"{obj.doctor.first_name} {obj.doctor.last_name}"
        return "Unknown Doctor"


# 👤 Patient Appointment View Serializer (includes doctor details)
class PatientAppointmentSerializer(serializers.ModelSerializer):
    """Serializer for patient viewing their appointments with doctor details"""
    doctor_details = DoctorDetailSerializer(source='doctor', read_only=True)
    slot_details = TimeSlotSerializer(source='slot', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor_details', 'slot', 'slot_details', 
            'patient_name', 'patient_phone', 'patient_email',
            'patient_age', 'patient_gender', 'patient_mrn',
            'patient_weight', 'patient_disease', 'patient_heart_rate', 
            'patient_blood_type', 'patient_photo',
            'appointment_type', 'location',
            'start_time', 'end_time', 'status', 
            'reschedule_reason', 'rejection_reason', 'created_at'
        ]
        read_only_fields = fields  # Patients can only view, not modify