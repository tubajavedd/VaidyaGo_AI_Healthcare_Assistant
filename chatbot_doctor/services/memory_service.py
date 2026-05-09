from chatbot_doctor.models import AdminChatMessage

class MemoryService:
    @staticmethod
    def get_memory_context(user, session, limit=5):
        """
        Retrieves recent conversation context.
        """
        messages = AdminChatMessage.objects.filter(session=session).order_by("-created_at")[:limit]
        context = []
        for msg in reversed(messages):
            context.append({"role": msg.sender, "content": msg.content})
        return context
