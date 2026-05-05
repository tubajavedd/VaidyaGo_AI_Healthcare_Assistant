from rest_framework import serializers
from .models import DoctorSlot

class DoctorSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorSlot
        fields = "__all__"

    def validate(self, data):
        if data['from_date'] > data['to_date']:
            raise serializers.ValidationError("From date cannot be after To date")

        if data['from_time'] >= data['to_time']:
            raise serializers.ValidationError("From time must be less than To time")

        if data['slot_duration'] not in [10, 15, 20, 30]:
            raise serializers.ValidationError(
                "Slot duration must be 10, 15, 20 or 30 minutes"
            )

        return data



from .models import TimeSlot

class TimeSlotSerializer(serializers.ModelSerializer):
    appointment_details = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start_time', 'end_time', 'is_booked', 'appointment_details']
        read_only_fields = ['id', 'is_booked']

    def get_appointment_details(self, obj):
        if not obj.is_booked:
            return None
        
        from appointments.models import Appointment
        appointment = Appointment.objects.filter(slot=obj).first()
        if appointment:
            return {
                "id": appointment.id,
                "patient_name": appointment.patient_name,
                "patient_phone": appointment.patient_phone,
                "status": appointment.status,
                "booked_by": "Vado Chatbot" if appointment.status == "booked" else "Manual Booking"
            }
        return None