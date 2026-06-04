from django.urls import path
from .views import (
    create_appointment, 
    list_appointments, 
    cancel_appointment, 
    reschedule_appointment, 
    reject_appointment, 
    accept_appointment, 
    pending_appointments,
    patient_appointments,
    patient_appointment_detail,
    recent_patients,
    complete_appointment,
    dashboard_stats,
    patient_gender_stats,
    patient_analytics_summary,
    patient_history
)

urlpatterns = [
    # Admin/Doctor endpoints
    path('appointments/', create_appointment),              # POST
    path('appointments/list/', list_appointments),          # GET
    path('appointments/stats/', dashboard_stats),           # GET
    path('appointments/gender-stats/', patient_gender_stats), # GET
    path('appointments/analytics-summary/', patient_analytics_summary), # GET
    path('appointments/history/', patient_history),         # GET
    path('appointments/pending/', pending_appointments),    # GET
    path('appointments/<int:id>/cancel/', cancel_appointment),  # PATCH
    path('appointments/<int:id>/accept/', accept_appointment),  # PATCH
    path('appointments/<int:id>/reject/', reject_appointment),  # PATCH
    path('appointments/<int:id>/reschedule/', reschedule_appointment),  # PATCH
    path('appointments/<int:id>/complete/', complete_appointment),  # PATCH
    path('appointments/recent/', recent_patients),          # GET
    
    # 👤 Patient endpoints (requires authentication)
    path('patient/appointments/', patient_appointments),  # GET - list all patient's appointments
    path('patient/appointments/<int:id>/', patient_appointment_detail),  # GET - get specific appointment detail

    # Alternate route to match /api/appointments/patient/appointments/
    path('appointments/patient/appointments/', patient_appointments),
    path('appointments/patient/appointments/<int:id>/', patient_appointment_detail),
]