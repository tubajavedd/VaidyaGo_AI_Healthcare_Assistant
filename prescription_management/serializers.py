from rest_framework import serializers
from .models import Prescription, PrescribedMedicine

class PrescribedMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescribedMedicine
        fields = ['id', 'name', 'dosage', 'frequency', 'duration_days', 'instructions']

class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescribedMedicineSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'patient',
            'image',
            'file',
            'document_type',
            'doctor_name',
            'hospital_name',
            'prescription_date',
            'extracted_patient_name',
            'summary',
            'findings',
            'test_results',
            'recommendations',
            'special_instructions',
            'status',
            'created_at',
            'updated_at',
            'medicines'
        ]
        read_only_fields = ['patient', 'status', 'created_at', 'updated_at']

class PrescriptionUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['image', 'file']

    def validate(self, data):
        if not data.get('image') and not data.get('file'):
            raise serializers.ValidationError("Either an image or a file must be provided.")
        return data
