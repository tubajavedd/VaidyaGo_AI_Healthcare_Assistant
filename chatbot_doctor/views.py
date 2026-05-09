import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from chatbot_doctor.services.chatbot_engine import ChatbotEngine
from chatbot_doctor.services.tools_registry import ToolsRegistry
from chatbot_doctor.serializers import AdminChatRequestSerializer, AdminChatResponseSerializer

logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def doctor_chat_view(request):
    """
    Main chat endpoint for doctors.
    """
    # Ensure the user is a doctor or admin
    if request.user.role not in ["DOCTOR", "ADMIN"]:
        return Response(
            {"success": False, "error": "Only doctors and admins can access the admin chatbot."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = AdminChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "error": "Invalid request", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    message = serializer.validated_data.get("message", "").strip()
    session_id = serializer.validated_data.get("session_id")
    audio_file = request.FILES.get("audio")

    # Handle Audio Transcription via Whisper
    if audio_file:
        from chatbot.services.voice_service import VoiceService
        transcription = VoiceService.transcribe(audio_file)
        if transcription:
            message = transcription
            logger.info(f"Doctor Whisper Transcription: {message}")

    try:
        response_data = ChatbotEngine.process(
            user=request.user,
            message=message,
            session_id=session_id
        )

        # Add Natural Voice URL via gTTS
        from chatbot.services.tts_service import TTSService
        response_data['audio_url'] = TTSService.generate_speech(response_data.get('reply', ''))

        response_serializer = AdminChatResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response({"success": True, **response_serializer.validated_data})
        
        return Response(
            {"success": False, "error": "Serialization error", "details": response_serializer.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        return Response(
            {"success": False, "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def doctor_tools_view(request):
    """
    Returns available tools for the admin chatbot.
    """
    return Response({
        "success": True,
        "tools": ToolsRegistry.get_all_tools(),
        "categories": ToolsRegistry.get_categories()
    })
