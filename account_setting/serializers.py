from rest_framework import serializers
from .models import AccountSettings


class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSettings
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
            "updated_at"
        ]
