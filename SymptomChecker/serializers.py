from rest_framework import serializers
from .models import Patient, DailySymptomVitals, SavedReport, SymptomAuditLog, MedicationDose

class SymptomVitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySymptomVitals
        fields = [
            'headache_duration', 'headache_severity',
            'fatigue_duration', 'fatigue_severity',
            'eye_strain_duration', 'eye_strain_severity',
            'temperature_f', 'heart_rate_bpm'
        ]

class PatientSummarySerializer(serializers.ModelSerializer):
    latest_symptoms = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'age', 'latest_symptoms']

    def get_latest_symptoms(self, obj):
        latest = obj.symptom_entries.first()
        if latest:
            return SymptomVitalsSerializer(latest).data
        return None

class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = ['id', 'condition_name', 'confidence_score', 'report_snapshot', 'saved_at']
        read_only_fields = ['saved_at']

class SymptomAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomAuditLog
        fields = ['id', 'active_symptoms', 'severity', 'environmental_triggers', 'additional_notes', 'created_at']
        read_only_fields = ['created_at']

class MedicationDoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationDose
        fields = ['id', 'medication_name', 'instructions', 'time_taken', 'date_taken', 'observation_notes', 'confirmed_at']
        read_only_fields = ['confirmed_at']























# from rest_framework import serializers
# from .models import SymptomLog

# class SymptomLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SymptomLog
#         fields = '__all__'
