from rest_framework import serializers
from .models import userDoc

class userDocSerializer(serializers.ModelSerializer):
    class Meta :
        model = userDoc
        fields='__all__'
        read_only_fields=['file_hash']
        