from chatbot.models import ChatMessage

class MemoryService:

    @staticmethod
    def save(user, message, response):
        ChatMessage.objects.create(
            user=user,
            message=message,
            response=response
        )

    @staticmethod
    def get_history(user, limit=5):
        return ChatMessage.objects.filter(user=user).order_by('-id')[:limit]
