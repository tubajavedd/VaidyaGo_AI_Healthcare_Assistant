from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_blank=True)
    session_id = serializers.IntegerField(required=False)
    document = serializers.FileField(required=False)
    documents = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        help_text="Upload multiple documents at once"
    )


class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
    session_id = serializers.IntegerField()
    intent = serializers.CharField()
    action = serializers.CharField(allow_null=True)
    data = serializers.DictField()
    action_executed = serializers.BooleanField()


class PrescriptionUploadSerializer(serializers.Serializer):
    """Serializer for prescription document uploads via chatbot"""
    documents = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        help_text="Medical documents (prescriptions, lab reports, etc.)"
    )
    document = serializers.FileField(required=False)
    
    class Meta:
        fields = ['documents', 'document']


class PrescriptionDetailSerializer(serializers.Serializer):
    """Serializer for prescription details response"""
    id = serializers.IntegerField()
    doctor_name = serializers.CharField()
    hospital_name = serializers.CharField()
    patient_name = serializers.CharField()
    prescription_date = serializers.DateField()
    medicines = serializers.ListField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
