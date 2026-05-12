import os
import sys

# Add the project root to sys.path to allow imports from chatbot
sys.path.append(os.getcwd())

# Mock Django settings if needed, or just import after setting DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
import django
django.setup()

from chatbot.services.tts_service import TTSService, COQUI_AVAILABLE

def test_tts():
    print(f"Coqui Available: {COQUI_AVAILABLE}")
    text = "Hello, I am your VaidyaGo assistant. How can I help you today?"
    
    print("Generating speech...")
    url = TTSService.generate_speech(text)
    
    if url:
        print(f"Success! Audio URL: {url}")
        # Check if file exists
        from django.conf import settings
        relative_path = url.replace(settings.MEDIA_URL, '')
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        if os.path.exists(full_path):
            print(f"File verified at: {full_path}")
            print(f"File size: {os.path.getsize(full_path)} bytes")
        else:
            print(f"File NOT found at: {full_path}")
    else:
        print("Failed to generate speech.")

if __name__ == "__main__":
    test_tts()
