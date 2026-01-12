from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.middleware.csrf import get_token
import json
from django.shortcuts import render


@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})


# ---------- SIGNUP ----------
@csrf_protect
def signup_view(request):
    if request.method == "POST":

        if not request.body:
            return JsonResponse({"error": "Empty request body"}, status=400)

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            return JsonResponse({"error": "Missing fields"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return JsonResponse({"message": "Signup successful", "user": username}, status=201)

    return render(request, "signup.html")


# ---------- LOGIN ----------
@csrf_protect
def login_view(request):
    if request.method == "POST":

        if not request.body:
            return JsonResponse({"error": "Empty request body"}, status=400)

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user": username})

        return JsonResponse({"error": "Invalid credentials"}, status=400)

    return render(request, "login.html")
