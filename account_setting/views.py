from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import AccountSettings
from .serializers import AccountSettingsSerializer


# ----------------------------
# GET + UPDATE SETTINGS
# ----------------------------
class AccountSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        settings, created = AccountSettings.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.get_full_name() or user.username,
                "email": user.email,
                "phone_number": "",
                "clinician_id": f"VG-{user.id:04d}-MED"
            }
        )
        return settings

    def get(self, request):
        settings = self.get_object(request.user)
        serializer = AccountSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        settings = self.get_object(request.user)

        serializer = AccountSettingsSerializer(
            settings,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


# ----------------------------
# CHANGE PASSWORD
# ----------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user)
        except Exception as e:
            return Response(
                {"error": list(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return Response({
            "message": "Password updated successfully"
        })


# ----------------------------
# TOGGLE 2FA
# ----------------------------
class Toggle2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        settings = request.user.account_settings
        settings.two_factor_enabled = not settings.two_factor_enabled
        settings.save()

        return Response({
            "two_factor_enabled": settings.two_factor_enabled
        })


# ----------------------------
# LOGIN HISTORY
# ----------------------------
class LoginHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = [
            {
                "device": "Chrome on Windows",
                "location": "Mumbai, India",
                "last_active": "2026-05-03 10:30 AM"
            },
            {
                "device": "Android App",
                "location": "Delhi, India",
                "last_active": "2026-05-02 09:15 PM"
            }
        ]

        return Response(sessions)


# ----------------------------
# DEACTIVATE ACCOUNT
# ----------------------------
class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        settings = user.account_settings

        settings.account_deactivated = True
        settings.save()

        user.is_active = False
        user.save()

        return Response({
            "message": "Account deactivated successfully"
        })


# ----------------------------
# REQUEST DATA DELETION
# ----------------------------
class RequestDataDeletionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        settings = request.user.account_settings
        settings.request_data_deletion = True
        settings.save()

        return Response({
            "message": "Data deletion request submitted"
        })
# ----------------------------
# SWITCH LANGUAGE
# ----------------------------
class SwitchLanguageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings, _ = AccountSettings.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        )
        return Response({
            "language": settings.language
        })

    def post(self, request):
        settings, _ = AccountSettings.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        )
        
        # Toggle between English and Hindi
        if "Hindi" in settings.language:
            settings.language = "English"
        else:
            settings.language = "Hindi"
            
        settings.save()
        return Response({
            "message": f"Language switched to {settings.language}",
            "language": settings.language
        })
