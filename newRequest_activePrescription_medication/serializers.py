from rest_framework import serializers
from .models import Medication, Pharmacy, PrescriptionRequest

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
<<<<<<< HEAD
        fields = ['id','name']
=======
        fields = '__all__'
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
<<<<<<< HEAD
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
=======
        fields = '__all__'


class PrescriptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionRequest
        fields = '__all__'
        read_only_fields = ['user']
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
