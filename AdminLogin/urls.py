from django.urls import path
from .views import admin_signup, admin_signup_page
from .views import AdminLoginView
from .views import AdminDoctorListCreateView, AdminDoctorUpdateView #doctor CRUD OPERATION
from .views import pending_doctors, approve_doctor, reject_doctor
from .views import send_otp, verify_otp, reset_password


urlpatterns = [
    # API endpoint for admin signup (POST request)
    path("api/admin/signup/", admin_signup, name="admin-signup-api"),

    # HTML page for admin signup form
    path("admin/signup/", admin_signup_page, name="admin-signup-page"),

    #login endpoint
    path('api/admin/login/', AdminLoginView.as_view(), name='admin-login'),

     path('api/admin/doctors/', AdminDoctorListCreateView.as_view()),
    path('api/admin/doctors/<int:id>/', AdminDoctorUpdateView.as_view()),


    path('doctors/pending/', pending_doctors),
    path('doctors/approve/<int:doctor_id>/', approve_doctor),
    path('doctors/reject/<int:doctor_id>/', reject_doctor),


    #otp
    path('send-otp/', send_otp),
    path('verify-otp/', verify_otp),
    path('reset-password/', reset_password),
]