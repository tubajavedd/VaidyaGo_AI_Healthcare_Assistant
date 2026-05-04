from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
    session_id = serializers.IntegerField(required=False)


class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
    session_id = serializers.IntegerField()
    intent = serializers.CharField()
    action = serializers.CharField(allow_null=True)
    data = serializers.DictField()
    action_executed = serializers.BooleanField()
