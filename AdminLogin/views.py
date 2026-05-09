import os
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
from django.core.mail import send_mail, EmailMessage

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import generate_username_from_email, generate_otp
from .models import Doctor, OTP, User
from Notifications.models import Notification
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

    data = json.loads(request.body)

    usertype = data.get("usertype")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # validate usertype
    if usertype == "admin":
        return JsonResponse(
            {"error": "Admin signup is not allowed"},
            status=403
        )

    if usertype not in ["patient", "doctor"]:
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

    if User.objects.filter(phone=phone).exists():
        return JsonResponse(
            {"error": "Phone number already exists"},
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

    if usertype == "admin":
        message = "admin signup successfully"
    elif usertype == "doctor":
        message = "doctor signup successfully"
    else:
        message = "patient signup successfully"

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    # Add role to token
    refresh["role"] = user.role
    access_token["role"] = user.role
    refresh["email"] = user.email
    refresh["username"] = user.username
    access_token["email"] = user.email
    access_token["username"] = user.username

    return JsonResponse({
        "message": message,
        "username": user.username,
        "access": str(access_token),
        "refresh": str(refresh),
        "user_id": user.id,
        "role": user.role,
        "redirectUrl": "/Form1" if usertype == "doctor" else "/login"
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
        access_token = refresh.access_token
        
        # Enforce admin role for specific email
        if user.email == getattr(settings, "ADMIN_EMAIL", None):
            refresh["role"] = "ADMIN"
            access_token["role"] = "ADMIN"
        else:
            refresh["role"] = user.role
            access_token["role"] = user.role

        refresh["email"] = user.email
        refresh["username"] = user.username
        access_token["email"] = user.email
        access_token["username"] = user.username

        role = user.role
        if user.email == getattr(settings, "ADMIN_EMAIL", None):
            role = "ADMIN"

        response_data = {
            "access": str(access_token),
            "refresh": str(refresh),
            "role": role,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "message": "Login successful",
            "id": user.id
        }

        if role == "DOCTOR":
            from Dr_personalInfo.models import DoctorPersonalInfo
            from django.db.models import Q
            query = Q(email=user.email)
            if hasattr(user, 'phone') and user.phone:
                query |= Q(mobile_number=user.phone)
            profile = DoctorPersonalInfo.objects.filter(query).first()
            if profile:
                response_data["doctor_id"] = profile.id
                response_data["first_name"] = profile.first_name
                response_data["last_name"] = profile.last_name
                response_data["full_name"] = f"{profile.first_name} {profile.last_name}".strip()

        return Response(response_data, status=status.HTTP_200_OK)


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


def serialize_doctor_full(d, request):
    docs = {}
    for doc in d.documents.all():
        docs[doc.document_type] = request.build_absolute_uri(doc.document_file.url) if doc.document_file else None
    
    # Defaults
    data = {
        "id": d.id,
        "name": f"{d.first_name} {d.last_name}".strip(),
        "first_name": d.first_name,
        "last_name": d.last_name,
        "phone": d.mobile_number,
        "email": d.email,
        "dob": d.date_of_birth.strftime('%Y-%m-%d') if d.date_of_birth else "N/A",
        "gender": d.gender,
        "city": d.city,
        "address": d.address,
        "status": d.status,
        "documents": docs,
        "specialization": "N/A",
        "experience": "N/A",
        "qualification": "N/A",
        "license_no": "N/A",
        "medical_council": "N/A",
        "employee_id": "N/A",
        "joining_date": "N/A",
        "employment_type": "N/A",
        "consultation_fees": "N/A",
        "leave_day": "N/A"
    }

    if hasattr(d, 'professional_info'):
        p = d.professional_info
        data.update({
            "specialization": p.specialization,
            "experience": f"{p.years_of_experience} years",
            "qualification": p.qualification,
            "license_no": p.medical_license_number,
            "medical_council": p.medical_council,
            "employee_id": p.doctor_employee_id
        })

    if hasattr(d, 'hospital_info'):
        h = d.hospital_info
        data.update({
            "joining_date": h.joining_date.strftime('%Y-%m-%d') if h.joining_date else "N/A",
            "employment_type": h.get_employment_type_display(),
            "consultation_fees": f"₹ {h.consultation_fees}",
            "leave_day": h.leave_day
        })
    
    return data

@api_view(["GET"])
@permission_classes([IsAdmin])
def pending_doctors(request):
    # Only show doctors who completed all forms and clicked Done on Form 4
    # Form 4 submission triggers /api/submit/<id>/ which sets status to 'pending'
    profile_doctors = DoctorPersonalInfo.objects.filter(status="pending")

    data = []
    for d in profile_doctors:
        data.append(serialize_doctor_full(d, request))

    return Response(data)




# ****************** APPROVE DOCTOR ******************
@api_view(["POST"])
@permission_classes([IsAdmin])
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

    if doctor.email:
        email_subject = "Your VaidyaGo Account has been Approved! 🎉"
        email_body = f"""
Hello Dr. {doctor.first_name},

Great news! Your application has been reviewed and approved by the VaidyaGo Admin team.

You can now log in to your dashboard and start managing your practice.

Login URL: {getattr(settings, "FRONTEND_URL", "http://localhost:5173")}/Finallogin

Welcome to the VaidyaGo family!

Best regards,
The VaidyaGo Team
"""
        
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "javedtuba1@gmail.com"),
            to=[doctor.email],
        )

        email.send(fail_silently=True)

        # Send in-app notification if user exists
        user = User.objects.filter(email=doctor.email).first()
        if user:
            Notification.objects.create(
                user=user,
                title="Application Approved",
                message="Admin approved you. You can now login."
            )

    return Response({"message": "Doctor approved"})


# ****************** REJECT DOCTOR ******************
@api_view(["POST"])
@permission_classes([IsAdmin])
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

    if doctor.email:
        email_subject = "Application Rejected"
        email_body = f"""
Your application has been rejected.

Reason: {reason}

Message: {message if message else "No additional message"}
        """
        
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            to=[doctor.email],
        )

        if doctor.rejected_file:
            try:
                # Ensure the file pointer is at the start if it was read before
                doctor.rejected_file.seek(0)
                email.attach(os.path.basename(doctor.rejected_file.name), doctor.rejected_file.read())
            except Exception:
                pass
        
        email.send(fail_silently=True)

        # Send in-app notification if user exists
        user = User.objects.filter(email=doctor.email).first()
        if user:
            Notification.objects.create(
                user=user,
                title="Application Rejected",
                message=f"Your application has been rejected. Reason: {reason}"
            )

    return Response({
        "message": "Doctor rejected and notified"
    })


@api_view(["GET"])
@permission_classes([IsAdmin])
def approved_doctors(request):
    doctors = DoctorPersonalInfo.objects.filter(status="approved")
    data = []
    for d in doctors:
        data.append(serialize_doctor_full(d, request))


    return Response(data)


@api_view(["GET"])
@permission_classes([IsAdmin])
def rejected_doctors(request):
    doctors = DoctorPersonalInfo.objects.filter(status="rejected")
    data = []
    for d in doctors:
        data.append(serialize_doctor_full(d, request))


    return Response(data)
