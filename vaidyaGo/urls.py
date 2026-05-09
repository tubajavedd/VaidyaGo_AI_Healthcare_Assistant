"""
URL configuration for vaidyaGo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("Auth.urls")),
    path('api/feedback/', include('feedback.urls')),
    path('accounts/', include('AdminLogin.urls')),
    path('api/admin/',include('adminProfile.urls')),
    path('api/', include('Dr_personalInfo.urls')),
    path('api/',include('Dr_professionalInfo.urls')),
    path('api/',include('Dr_hospitalInfo.urls')),
    path('api/', include('Dr_Documents.urls')),
    path('api/', include('DoctorSlot.urls')),
    path('api/', include('appointments.urls')),
    path('reminder/', include('reminder.urls')),
    path('payment/',include('payment.urls')),
    path('notifications/', include('Notifications.urls')),
    path('today-schedule/', include('TodaySchedule_medication.urls')),
    path('api/prescriptions/', include('newRequest_activePrescription_medication.urls')),
    path('api/', include('AddPastMedication.urls')),
    path("api/vado/", include("chatbot.urls")),
    path("api/vado-doctor/", include("chatbot_doctor.urls")),
    path("api/vado-admin/", include("chatbot_admin.urls")),
    path("update/", include('updateLog_medication.urls')),
    path("api/", include("account_setting.urls")),
    path('profile/',include('editProfile.urls')),
    path('api/', include('prescription_management.urls')),
    path('api/symptomchecker/', include('SymptomChecker.urls')),

]
