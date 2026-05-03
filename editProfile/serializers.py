from rest_framework import serializers
from .models import editProfile

class editProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=editProfile
        fields="__all__"
        read_only_fields=[
            "user",
            "created_at",
            "updated_at"
        ]