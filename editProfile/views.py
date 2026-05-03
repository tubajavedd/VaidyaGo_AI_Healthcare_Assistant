from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import editProfile
from .serializers import editProfileSerializers


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, user):
        profile, created = editProfile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.get_full_name() or user.username,
                "email": user.email,
                "phone_number": "",
                "residential_address": "",
                "emergency_contact_name": "",
                "emergency_contact_number": "",
            }
        )
        return profile

    def get(self, request):
        profile = self.get_object(request.user)
        serializer = editProfileSerializers(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object(request.user)

        serializer = editProfileSerializers(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
