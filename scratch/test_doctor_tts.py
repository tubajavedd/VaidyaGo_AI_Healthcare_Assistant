import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from chatbot_doctor.services.chatbot_engine import ChatbotEngine
from chatbot.services.tts_service import TTSService
from chatbot_doctor.serializers import AdminChatResponseSerializer

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.filter(role='DOCTOR').first() or User.objects.first()

    message = "hi"
    print(f"User: {user}")
    response_data = ChatbotEngine.process(user=user, message=message, session_id=None)
    print("Response Data:", response_data)

    audio_url = TTSService.generate_speech(response_data.get('reply', ''))
    response_data['audio_url'] = audio_url
    print("Audio URL:", audio_url)

    response_serializer = AdminChatResponseSerializer(data=response_data)
    if response_serializer.is_valid():
        print("Success:", response_serializer.validated_data)
    else:
        print("Serialization Error:", response_serializer.errors)

except Exception as e:
    import traceback
    traceback.print_exc()
