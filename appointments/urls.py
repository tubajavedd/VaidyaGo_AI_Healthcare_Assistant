from django.urls import path
from .views import create_appointment, list_appointments, cancel_appointment, reschedule_appointment, reject_appointment, accept_appointment, pending_appointments

urlpatterns = [
    path('appointments/', create_appointment),              # POST
    path('appointments/list/', list_appointments),          # GET
    path('appointments/pending/', pending_appointments),    # GET
    path('appointments/<int:id>/cancel/', cancel_appointment),  # PATCH
    path('appointments/<int:id>/accept/', accept_appointment),  # PATCH
    path('appointments/<int:id>/reject/', reject_appointment),  # PATCH
    path('appointments/<int:id>/reschedule/', reschedule_appointment),
]