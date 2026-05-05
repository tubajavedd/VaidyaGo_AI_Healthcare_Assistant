from django.urls import path
from .views import signup_view, login_view, csrf_token_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("csrf-token/", csrf_token_view, name="csrf_token"),
]
