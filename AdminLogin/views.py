import jwt
import json
import phonenumbers

from phonenumbers import NumberParseException
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import send_mail

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import generate_username_from_email, generate_otp
from .models import Doctor, OTP
from .serializers import DoctorSerializer, AdminLoginSerializer
from .permissions import IsAdmin
from Dr_personalInfo.models import DoctorPersonalInfo


User = get_user_model()


# ******************** DOCTOR CRUD ********************
class AdminDoctorListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Doctor created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDoctorUpdateView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, id):
        doctor = get_object_or_404(Doctor, id=id)
        serializer = DoctorSerializer(
            doctor,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Doctor updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ****************** SIGNUP ******************
@csrf_exempt
def admin_signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    if not getattr(settings, "ALLOW_ADMIN_SIGNUP", False):
        return JsonResponse(
            {"error": "Admin signup is disabled"},
            status=403
        )

    data = json.loads(request.body)

    usertype = data.get("usertype")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # validate usertype
    if usertype not in ["patient", "admin", "doctor"]:
        return JsonResponse(
            {"error": "Invalid usertype"},
            status=400
        )

    # validate required fields
    if not all([email, phone, password, confirm_password]):
        return JsonResponse(
            {"error": "All fields are required"},
            status=400
        )

    if password != confirm_password:
        return JsonResponse(
            {"error": "Passwords do not match"},
            status=400
        )

    if User.objects.filter(email=email).exists():
        return JsonResponse(
            {"error": "Email already exists"},
            status=400
        )

    # phone validation
    try:
        parsed_number = phonenumbers.parse(phone, None)

        if not phonenumbers.is_valid_number(parsed_number):
            return JsonResponse(
                {"error": "Invalid phone number"},
                status=400
            )

        phone = phonenumbers.format_number(
            parsed_number,
            phonenumbers.PhoneNumberFormat.E164
        )

    except NumberParseException:
        return JsonResponse(
            {"error": "Invalid phone format"},
            status=400
        )

    # role logic
    if usertype == "admin":
        role = "ADMIN"
        is_staff = True
        is_superuser = True

    elif usertype == "doctor":
        role = "DOCTOR"
        is_staff = False
        is_superuser = False

    else:
        role = "PATIENT"
        is_staff = False
        is_superuser = False

    username = generate_username_from_email(email)

    user = User.objects.create(
        username=username,
        role=role,
        email=email,
        phone=phone,
        is_staff=is_staff,
        is_superuser=is_superuser,
        password=make_password(password)
    )

    payload = {
        "user_id": user.id,
        "role": user.role,
        "email": user.email,
        "phone": user.phone,
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    if usertype == "admin":
        message = "admin signup successfully"
    elif usertype == "doctor":
        message = "doctor signup successfully"
    else:
        message = "patient signup successfully"

    return JsonResponse({
        "message": message,
        "username": user.username,
        "token": token
    }, status=201)


def admin_signup_page(request):
    return render(request, "admin_signup.html")


# ****************** LOGIN ******************
class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        # custom refresh token claims
        refresh["role"] = user.role
        refresh["email"] = user.email
        refresh["username"] = user.username

        access_token = refresh.access_token
        access_token["role"] = user.role
        access_token["email"] = user.email
        access_token["username"] = user.username

        return Response({
            "access": str(access_token),
            "refresh": str(refresh),
            "role": user.role,
            "username": user.username,
            "message": "Login successful"
        }, status=status.HTTP_200_OK)


# ****************** SEND OTP ******************
@api_view(["POST"])
def send_otp(request):
    email = request.data.get("email")
    otp = generate_otp()

    if email:
        OTP.objects.create(email=email, otp=otp)

        send_mail(
            "VaidyaGo",
            f"Your OTP is {otp}",
            "javedtuba1@gmail.com",
            [email],
            fail_silently=False,
        )
        return Response({"message": "OTP sent to email"})

    return Response({"error": "Provide email"})


# ****************** VERIFY OTP ******************
@api_view(["POST"])
def verify_otp(request):
    otp = request.data.get("otp")

    otp_obj = OTP.objects.filter(otp=otp).last()

    if not otp_obj:
        return Response({"error": "Invalid OTP"})

    if timezone.now() - otp_obj.created_at > timedelta(minutes=5):
        return Response({"error": "OTP expired"})

    otp_obj.is_verified = True
    otp_obj.save()

    return Response({"message": "OTP verified"})


# ****************** RESET PASSWORD ******************
@api_view(["POST"])
def reset_password(request):
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

    if not email or not password or not confirm_password:
        return Response({"error": "All fields are required"})

    email = email.strip().lower()

    if password != confirm_password:
        return Response({"error": "Passwords do not match"})

    otp_obj = OTP.objects.filter(
        email__iexact=email,
        is_verified=True
    ).last()

    if not otp_obj:
        return Response({"error": "OTP not verified for this email"})

    if timezone.now() - otp_obj.created_at > timedelta(minutes=5):
        return Response({"error": "OTP expired"})

    user = User.objects.filter(email__iexact=email).first()

    if not user:
        return Response({"error": "User not found"})

    user.set_password(password)
    user.save()

    OTP.objects.filter(email__iexact=email).delete()

    return Response({"message": "Password updated successfully"})


# ****************** GET PENDING DOCTORS ******************
@api_view(["GET"])
@permission_classes([IsAdminUser])
def pending_doctors(request):
    DoctorPersonalInfo.objects.filter(
        status="incomplete"
    ).update(status="pending")

    doctors = DoctorPersonalInfo.objects.filter(status="pending")

    data = []
    for d in doctors:
        data.append({
            "id": d.id,
            "name": f"{d.first_name} {d.last_name}".strip(),
            "status": d.status
        })

    return Response(data)


# ****************** APPROVE DOCTOR ******************
@api_view(["POST"])
@permission_classes([IsAdminUser])
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(
        DoctorPersonalInfo,
        id=doctor_id
    )

    if doctor.status == "approved":
        return Response(
            {"error": "Doctor already approved"},
            status=400
        )

    doctor.status = "approved"
    doctor.rejected_reason = None
    doctor.rejected_message = None
    doctor.rejected_file = None
    doctor.save()

    if doctor.user and doctor.user.email:
        send_mail(
            subject="Application Approved",
            message="Your doctor profile has been approved. You can now access the system.",
            from_email=getattr(
                settings,
                "DEFAULT_FROM_EMAIL",
                None
            ),
            recipient_list=[doctor.user.email],
            fail_silently=True,
        )

    return Response({"message": "Doctor approved"})


# ****************** REJECT DOCTOR ******************
@api_view(["POST"])
@permission_classes([IsAdminUser])
def reject_doctor(request, doctor_id):
    doctor = get_object_or_404(
        DoctorPersonalInfo,
        id=doctor_id
    )

    reason = request.data.get("reason")
    message = request.data.get("message")
    file = request.FILES.get("file")

    if not reason:
        return Response(
            {"error": "Reason is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if doctor.status == "rejected":
        return Response(
            {"error": "Doctor already rejected"},
            status=400
        )

    doctor.status = "rejected"
    doctor.rejected_reason = reason
    doctor.rejected_message = message
    doctor.rejected_file = file
    doctor.save()

    if doctor.user and doctor.user.email:
        send_mail(
            subject="Application Rejected",
            message=f"""
Your application has been rejected.

Reason: {reason}

Message: {message if message else "No additional message"}
            """,
            from_email=getattr(
                settings,
                "DEFAULT_FROM_EMAIL",
                None
            ),
            recipient_list=[doctor.user.email],
            fail_silently=False,
        )

    return Response({
        "message": "Doctor rejected and notified"
    })
