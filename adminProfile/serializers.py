from rest_framework import serializers
from .models import Profile, Address
from django.contrib.auth.models import User

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city', 'pincode']

class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(source="user.address")

    class Meta:
        model = Profile
        fields = ['phone_number', 'post', 'language', 'google_connected', 'google_email', 'address']
