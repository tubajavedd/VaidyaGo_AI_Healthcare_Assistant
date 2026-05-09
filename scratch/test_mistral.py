import os
import django
import sys

# Set up Django environment
sys.path.append('d:\\directory\\UPDATED_VAIDYAGO\\vaidyaGo\\vaidyaGo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from chatbot_doctor.services.mistral_service import MistralService

print(f"MISTRAL_API_KEY: {os.getenv('MISTRAL_API_KEY')[:5]}...")
try:
    response = MistralService.generate_response("Hi", "You are a helpful assistant")
    print(f"Mistral Response: {response}")
except Exception as e:
    print(f"Error: {str(e)}")
