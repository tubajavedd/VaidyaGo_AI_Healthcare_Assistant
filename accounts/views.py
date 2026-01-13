import jwt
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_username_from_email

User = get_user_model()

# ------------------- API -------------------
@csrf_exempt
def admin_signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    # Only allow if ENV FLAG is true
    if not getattr(settings, "ALLOW_ADMIN_SIGNUP", False):
        return JsonResponse({"error": "Admin signup is disabled"}, status=403)

    data = json.loads(request.body)

    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # ---------------- Validation ----------------
    if not all([ email, phone, password, confirm_password]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    if password != confirm_password:
        return JsonResponse({"error": "Passwords do not match"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    if User.objects.filter(phone=phone).exists():
        return JsonResponse({"error": "Phone already exists"}, status=400)

    # ---------------- Create Admin ----------------
    username = generate_username_from_email(email)
    user = User.objects.create(
        username=username,
        role="ADMIN",
        email=email,
        phone=phone,
        is_staff=True,
        is_superuser=True,
        password=make_password(password)
    )

    # ---------------- JWT Token ----------------
    payload = {
        "user_id": user.id,
        "role": user.role,
        "email":user.email,
        "phone":user.phone,
        "exp": datetime.utcnow() + timedelta(min==30),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return JsonResponse({
        "message": "Admin created successfully",
         "username": user.username,
        "token": token
    }, status=201)

# ------------------- HTML Page -------------------
def admin_signup_page(request):
    return render(request, "admin_signup.html")


#********LOGIN*************

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdminLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
