from django.urls import path
from .views import (
    DoctorSlotListCreateAPI,
    DoctorSlotDetailAPI,
    DoctorAllSlotsAPI,
    DoctorBookedSlotsAPI,
    GenerateSlotsAPI
)
urlpatterns = [
    path('doctor-slots/', DoctorSlotListCreateAPI.as_view()),
    path('doctor-slots/<int:pk>/', DoctorSlotDetailAPI.as_view()),
    path('generate/', GenerateSlotsAPI.as_view(), name='generate_slots_api'),
    path('doctor/<int:doctor_id>/slots/booked/', DoctorBookedSlotsAPI.as_view()), # only booked
    path('doctor/<int:doctor_id>/slots/', DoctorAllSlotsAPI.as_view()),         # all slots
]

