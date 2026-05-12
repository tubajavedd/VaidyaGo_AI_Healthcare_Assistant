from django.urls import path
from .views import admin_signup, admin_signup_page
from .views import AdminLoginView
from .views import AdminDoctorListCreateView, AdminDoctorUpdateView #doctor CRUD OPERATION
from .views import pending_doctors, approve_doctor, reject_doctor, approved_doctors, rejected_doctors
from .views import send_otp, verify_otp, reset_password
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    # signup/login for all users
    path("api/signup/", admin_signup, name="signup-api"),
    path('api/login/', AdminLoginView.as_view(), name='login'),#login for all users (admin, doctor, patient) with role-based access control
    
    #admin doctor crud operation(admin manages doctor records mannually)
    path('api/admin/doctors/', AdminDoctorListCreateView.as_view()),#admin add dcotors mannually and also get list of doctors
    path('api/admin/doctors/<int:id>/', AdminDoctorUpdateView.as_view()),#admin update doctor details and also delete doctor records

    #dcotor approval process
    path('doctors/pending/', pending_doctors),
    path('doctors/approved/', approved_doctors),
    path('doctors/rejected/', rejected_doctors),
    path('doctors/approve/<int:doctor_id>/', approve_doctor),
    path('doctors/reject/<int:doctor_id>/', reject_doctor),


    #otp +password reset
    path('send-otp/', send_otp),
    path('verify-otp/', verify_otp),
    path('reset-password/', reset_password),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]