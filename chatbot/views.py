from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from chatbot.serializers import ChatRequestSerializer
from chatbot.services.chatbot_engine import ChatbotEngine


class ChatAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        session_id = serializer.validated_data.get("session_id")

        user = request.user

        if not user.is_authenticated:
            User = get_user_model()

            user, _ = User.objects.get_or_create(
                username="test_user",
                defaults={
                    "email": "test@test.com"
                }
            )

        result = ChatbotEngine.process(
            user=user,
            message=message,
            session_id=session_id
        )

        return Response(result)
