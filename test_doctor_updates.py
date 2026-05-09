import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from AdminLogin.models import User
from chatbot_doctor.services.chatbot_engine import ChatbotEngine
from Dr_personalInfo.models import DoctorPersonalInfo

def test_doctor_updates():
    user = User.objects.get(username="admin_javedtuba")
    print(f"Testing Doctor Updates for: {user.username}")
    
    # 1. Update City
    print("\nTest 1: Update City")
    response = ChatbotEngine.process(user, "Update my city to 'New Delhi'.")
    print(f"Assistant: {response['reply']}")
    print(f"Action: {response['action']}")
    
    # Verify in DB
    doctor = DoctorPersonalInfo.objects.get(email=user.email)
    print(f"Current City in DB: {doctor.city}")

    # 2. Reminder Test
    print("\nTest 2: Appointment Reminder")
    response = ChatbotEngine.process(user, "Remind me about my appointments today.")
    print(f"Assistant: {response['reply']}")
    print(f"Action: {response['action']}")

if __name__ == "__main__":
    test_doctor_updates()
