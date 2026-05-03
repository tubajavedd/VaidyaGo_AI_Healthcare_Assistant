from rest_framework import serializers
from .models import UpdateLog, AccountSettings


class UpdateLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = UpdateLog
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSettings
        fields = "__all__"
        read_only_fields = ["user"]
