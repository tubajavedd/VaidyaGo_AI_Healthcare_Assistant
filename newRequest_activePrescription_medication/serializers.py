from rest_framework import serializers
from .models import Medication, Pharmacy, PrescriptionRequest

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id','name']


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields =['id','name','address','phone']


class PrescriptionRequestSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source="medication.name", read_only=True)
    pharmacy_name = serializers.CharField(source="pharmacy.name", read_only=True)

    class Meta:
        model = PrescriptionRequest
        fields = [
            "id",
            "medication",
            "medication_name",
            "pharmacy",
            "pharmacy_name",
            "delivery_preference",
            "created_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return PrescriptionRequest.objects.create(patient=user, **validated_data)