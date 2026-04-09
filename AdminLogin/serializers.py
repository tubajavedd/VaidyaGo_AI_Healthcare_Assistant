from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'phone',
            'specialty',
            'experience',
            'is_active'
        ]



#****************SIGNUP***********
class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ 'email', 'phone', 'password']

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


#*****************LOGIN**************

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        phone = data.get('phone', None)
        password = data.get('password')

        user = None

        if email:
            user = authenticate(email=email, password=password)
        elif phone:
            user = authenticate(phone=phone, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if user.role != 'ADMIN':
            raise serializers.ValidationError("User is not an admin")
        
        data['user'] = user
        return data
