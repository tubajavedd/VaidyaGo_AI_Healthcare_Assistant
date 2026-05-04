from chatbot.models import ChatMessage


class MemoryService:
    @staticmethod
    def get_memory_context(user=None, session=None, limit=5):
        if session is not None:
            messages = ChatMessage.objects.filter(session=session)
        elif user is not None:
            messages = ChatMessage.objects.filter(session__user=user)
        else:
            return "No memory available."

        messages = messages.order_by("-created_at")[:limit]
        history = []
        for msg in reversed(messages):
            history.append(f"{msg.sender}: {msg.content}")

        return "\n".join(history)

    @staticmethod
    def save_interaction(session, user_message, assistant_message, language="en"):
        ChatMessage.objects.create(
            session=session,
            sender="user",
            content=user_message,
            language=language,
        )
        ChatMessage.objects.create(
            session=session,
            sender="assistant",
            content=assistant_message,
            language=language,
        )
