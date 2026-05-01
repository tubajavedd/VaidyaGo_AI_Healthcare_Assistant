from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
    session_id = serializers.IntegerField(required=False)


class ChatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
    session_id = serializers.IntegerField()
