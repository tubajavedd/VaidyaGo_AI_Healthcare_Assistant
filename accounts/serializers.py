from rest_framework import serializers
from .models import User

class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.role = 'ADMIN'
        user.is_staff = True
        user.set_password(password)  # 🔐 HASH
        user.save()
        return user
