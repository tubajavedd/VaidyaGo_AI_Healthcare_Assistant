from rest_framework import serializers
from .models import Reminder, FCMToken

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = ['next_reminder_datetime', 'user', 'is_active', 'snooze_until']

class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ['token']
