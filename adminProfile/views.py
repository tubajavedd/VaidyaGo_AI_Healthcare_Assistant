from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from AdminLogin.models import Profile, Address
from .serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail


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

#get submitted doctor(get notification of doctor who submitted)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from Dr_personalInfo.models import DoctorPersonalInfo

@api_view(['GET'])
@permission_classes([IsAdminUser])
def pending_doctors(request):
    doctors = DoctorPersonalInfo.objects.filter(status='submitted')

    data = []
    for d in doctors:
        data.append({
            "id": d.id,
            "name": f"{d.first_name} {d.last_name}".strip(),
            "status": d.status
        })

    return Response(data)


#approve doctor
@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorPersonalInfo, id=doctor_id)

    doctor.status = 'approved'
    doctor.rejected_reason = None
    doctor.rejected_message = None
    doctor.rejected_file = None
    doctor.save()

    return Response({"message": "Doctor approved"})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorPersonalInfo, id=doctor_id)

    reason = request.data.get('reason')
    message = request.data.get('message')
    file = request.FILES.get('file')

    if not reason:
        return Response({"error": "Reason is required"}, status=status.HTTP_400_BAD_REQUEST)

    doctor.status = 'rejected'
    doctor.rejected_reason = reason
    doctor.rejected_message = message
    doctor.rejected_file = file
    doctor.save()

    send_mail(
        subject="Application Rejected",
        message=f"""
Your application has been rejected.

Reason: {reason}

Message: {message if message else "No additional message"}
        """,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[doctor.email],
        fail_silently=False,
    )

    return Response({"message": "Doctor rejected and notified"})
