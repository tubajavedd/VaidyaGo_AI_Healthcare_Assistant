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
