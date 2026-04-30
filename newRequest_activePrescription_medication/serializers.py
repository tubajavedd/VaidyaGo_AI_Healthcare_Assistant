from rest_framework import serializers
from .models import Medication, Pharmacy, PrescriptionRequest

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'


class PrescriptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionRequest
        fields = '__all__'
        read_only_fields = ['user']