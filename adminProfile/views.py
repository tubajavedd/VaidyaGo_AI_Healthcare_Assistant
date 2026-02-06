from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile, Address
from .serializers import ProfileSerializer


class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        address, _ = Address.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        address, _ = Address.objects.get_or_create(user=request.user)

        profile.phone_number = request.data.get('phone_number')
        profile.post = request.data.get('post')
        profile.language = request.data.get('language')

        address_data = request.data.get('address', {})
        address.country = address_data.get('country')
        address.city = address_data.get('city')
        address.pincode = address_data.get('pincode')

        profile.save()
        address.save()

        return Response({"message": "Profile updated successfully"}, status=200)


class DisconnectGoogle(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        profile.google_connected = False
        profile.google_email = None
        profile.save()

        return Response({"message": "Google account disconnected"})
