from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Doctor

User = get_user_model()

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
        fields = [ 'usertype','email', 'phone', 'password']
    

    def validate_usertype(self, value):
        if value not in ['patient', 'admin', 'doctor']:
           raise serializers.ValidationError("Invalid usertype")
        return value

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
        usertype = validated_data.get('usertype')

        user = User(**validated_data)
        if usertype=='admin':
           user.role='ADMIN'
           user.is_staff=True
        elif usertype=='doctor':
            user.role='DOCTOR'
        else:
            user.role='PATIENT'
    
        user.set_password(password)  # 🔐 HASH
        user.save()
        return user


#*****************LOGIN**************

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        phone = data.get('phone', None)
        username = data.get('username', None)
        password = data.get('password')

        if not any([email, phone, username]):
            raise serializers.ValidationError(
                "Provide email, phone, or username with password."
            )

        user = None
        if email:
            user = User.objects.filter(email=email).first()
        elif phone:
            user = User.objects.filter(phone=phone).first()
        elif username:
            user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")

        data['user'] = user
        return data

