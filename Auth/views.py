import jwt
import json
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
from datetime import datetime, timedelta


# ================= CSRF TOKEN =================
@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})


# ================= REAL JWT GENERATOR =================
def generate_jwt(user):
    phone = None
    if hasattr(user, "userprofile"):
        phone = user.userprofile.phone

    payload = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": phone,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token
# ================= JWT VERIFY DECORATOR =================
def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")

        if not token:
            return JsonResponse({"error": "Token missing"}, status=401)

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            request.user_id = payload["user_id"]
            request.username = payload["username"]

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper



# ================= SIGNUP =================
@csrf_exempt
def signup_view(request):
    if request.method == "POST" and request.content_type.startswith("application/json"):
        try:
            data = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        confirm_password = data.get("confirm_password")  # ✅ NEW

        if not all([username, email, phone, password, confirm_password]):
            return JsonResponse({"error": "All fields required"}, status=400)

        # ✅ confirm password check
        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            phone=phone
        )

        token = generate_jwt(user)

        return JsonResponse({
            "message": "Signup successful",
            "token": token
        }, status=201)

    return render(request, "signup.html")

# ================= LOGIN =================
@csrf_exempt
def login_view(request):
    if request.method == "POST" and request.content_type.startswith("application/json"):
        try:
            data = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

        token = generate_jwt(user)

        response = JsonResponse({
            "message": "Login successful"
        },status=201)

        # ✅ Store token secretly
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,   # JS cannot access
            secure=True,     # HTTPS only
            samesite="Strict"
        )

        return response

    return render(request, "login.html")


# ================= PROTECTED =================
@jwt_required
def profile_view(request):
    return JsonResponse({
        "message": "JWT verified successfully",
        "user_id": request.user_id,
        "username": request.username
    })
