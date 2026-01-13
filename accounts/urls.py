from django.urls import path
from .views import admin_signup, admin_signup_page
from .views import AdminLoginView
urlpatterns = [
    # API endpoint for admin signup (POST request)
    path("api/admin/signup/", admin_signup, name="admin-signup-api"),

    # HTML page for admin signup form
    path("admin/signup/", admin_signup_page, name="admin-signup-page"),

    #login endpoint
    path('api/admin/login/', AdminLoginView.as_view(), name='admin-login'),
]
