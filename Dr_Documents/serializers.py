from rest_framework import serializers
from .models import DoctorDocument


class DoctorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDocument
        fields = [
            'id',
            'document_type',
            'document_file',
            'uploaded_at'
        ]

        read_only_fields = ['id', 'uploaded_at']
