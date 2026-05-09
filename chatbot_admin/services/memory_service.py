from chatbot_admin.models import AdminChatMessage

class MemoryService:
    @staticmethod
    def get_memory_context(user, session):
        """
        Retrieves recent history or relevant context for the current session.
        """
        recent_msgs = AdminChatMessage.objects.filter(session=session).order_by('-created_at')[:5]
        if not recent_msgs.exists():
            return "No previous context in this session."
        
        context = "Recent interaction: " + " | ".join([f"{m.sender}: {m.content[:50]}" for m in reversed(recent_msgs)])
        return context
