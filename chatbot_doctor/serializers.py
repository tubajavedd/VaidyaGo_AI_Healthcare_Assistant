from rest_framework import serializers

class AdminChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    session_id = serializers.IntegerField(required=False, allow_null=True)
    doctor_id = serializers.IntegerField(required=False, allow_null=True)

class AdminChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
    session_id = serializers.IntegerField()
    intent = serializers.CharField()
    action = serializers.CharField(required=False, allow_null=True)
    data = serializers.DictField()
    action_executed = serializers.BooleanField()
    audio_url = serializers.CharField(allow_null=True, required=False)
