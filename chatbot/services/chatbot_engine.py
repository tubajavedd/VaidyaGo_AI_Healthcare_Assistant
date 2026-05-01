from chatbot.models import ChatSession, ChatMessage
from chatbot.services.language_service import LanguageService
from chatbot.services.memory_service import MemoryService
from chatbot.services.prompt_service import PromptService
from chatbot.services.llm_service import LLMService


class ChatbotEngine:

    @staticmethod
    def process(user, message, session_id=None):

        lower_message = message.lower().strip()

        greetings = ["hi", "hello", "hey", "hii", "namaste"]

        # ✅ 1. GREETING SHORT-CIRCUIT (FAST RESPONSE)
        if lower_message in greetings:
            reply = "Hello, I'm Vado. What may I help you with today?"

            # session handling still needed
            if session_id:
                session = ChatSession.objects.get(id=session_id, user=user)
            else:
                session = ChatSession.objects.create(user=user)

            # save chat
            ChatMessage.objects.create(
                session=session,
                sender="user",
                content=message,
                language="en"
            )

            ChatMessage.objects.create(
                session=session,
                sender="assistant",
                content=reply,
                language="en"
            )

            return {
                "reply": reply,
                "session_id": session.id
            }

        # ✅ 2. NORMAL FLOW (FULL PIPELINE)

        language = LanguageService.detect_language(message)

        if session_id:
            session = ChatSession.objects.get(id=session_id, user=user)
        else:
            session = ChatSession.objects.create(user=user)

        MemoryService.extract_and_store(user, message)

        memory_context = MemoryService.get_memory_context(user)

        ChatMessage.objects.create(
            session=session,
            sender="user",
            content=message,
            language=language
        )

        messages = ChatMessage.objects.filter(
            session=session
        ).order_by("-created_at")[:5]

        history = "\n".join([
            f"{msg.sender}: {msg.content}"
            for msg in reversed(messages)
        ])

        prompt = PromptService.build_prompt(
            message=message,
            memory=memory_context,
            history=history
        )

        reply = LLMService.generate_response(prompt)

        ChatMessage.objects.create(
            session=session,
            sender="assistant",
            content=reply,
            language=language
        )

        return {
            "reply": reply,
            "session_id": session.id
        }
