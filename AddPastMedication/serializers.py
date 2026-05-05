from rest_framework import serializers
from .models import PastMedication, Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name"]


class PastMedicationSerializer(serializers.ModelSerializer):
    prescribing_doctor_name = serializers.CharField(source="prescribing_doctor.name", read_only=True)

    class Meta:
        model = PastMedication
        fields = [
            "id",
            "medication_name",
            "dosage",
            "prescribing_doctor",
            "prescribing_doctor_name",
            "start_date",
            "end_date",
            "reason",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return PastMedication.objects.create(patient=user, **validated_data)