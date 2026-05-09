from django.urls import path
from chatbot_doctor.views import doctor_chat_view, doctor_tools_view

urlpatterns = [
    path("chat/", doctor_chat_view, name="doctor-chat"),
    path("tools/", doctor_tools_view, name="doctor-tools"),
]
