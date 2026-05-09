import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from AdminLogin.models import User
from chatbot_doctor.services.chatbot_engine import ChatbotEngine
from appointments.models import Appointment
from DoctorSlot.models import TimeSlot
from Dr_personalInfo.models import DoctorPersonalInfo

def test_doctor_flow():
    user = User.objects.get(username="admin_javedtuba")
    doctor = DoctorPersonalInfo.objects.get(email=user.email)
    print(f"Testing Doctor Flow for: {user.username} (Dr. {doctor.first_name})")
    
    # 1. Check Notifications
    print("\nTest 1: Notifications")
    response = ChatbotEngine.process(user, "Do I have any new notifications?")
    print(f"Assistant: {response['reply']}")
    print(f"Action: {response['action']}")

    # 2. Check Professional Info
    print("\nTest 2: Professional Info")
    response = ChatbotEngine.process(user, "What is my specialization?")
    print(f"Assistant: {response['reply']}")

    # 3. Appointment Management (requires an appointment)
    # We'll just check if it detects the intent
    print("\nTest 3: Intent Detection for Rejecting Appointment")
    response = ChatbotEngine.process(user, "Reject appointment 5 because I will be in surgery.")
    print(f"Assistant: {response['reply']}")
    print(f"Action: {response['action']}, Data: {response.get('data')}")

if __name__ == "__main__":
    test_doctor_flow()
