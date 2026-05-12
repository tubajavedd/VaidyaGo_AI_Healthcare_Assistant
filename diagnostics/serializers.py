from rest_framework import serializers
from .models import Diagnostic

class DiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = '__all__'
        read_only_fields = ['user', 'possible_diseases', 'recommendations', 'precautions', 'consultation_advice', 'confidence_score', 'ai_response', 'created_at', 'updated_at']

class DiagnosticRequestSerializer(serializers.Serializer):
    body_part = serializers.CharField(max_length=100)
    sub_region = serializers.CharField(max_length=100)
    symptoms = serializers.ListField(child=serializers.CharField())
    duration = serializers.CharField(max_length=100)
    severity = serializers.CharField(max_length=50)
