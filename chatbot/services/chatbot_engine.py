import logging
import re

from chatbot.models import ChatSession, ChatMessage
from chatbot.services.language_service import LanguageService
from chatbot.services.memory_service import MemoryService
from chatbot.services.prompt_service import PromptService
from chatbot.services.llm_service import LLMService
from chatbot.services.intent_service import IntentService
from chatbot.services.agent_manager import AgentManager

logger = logging.getLogger(__name__)


class ChatbotEngine:
    """
    Main chatbot orchestrator.

    Flow:
    1. Save user message
    2. Build prompt
    3. Get LLM response
    4. Parse intent
    5. Agent manager routes actions
    6. Save assistant response
    """

    GREETINGS = {"hi", "hello", "hey", "hii", "namaste"}

    @staticmethod
    def process(user, message, session_id=None):
        try:
            # Sanitize message: Keep only alphabets and digits from ANY language (Unicode) and spaces
            # \w matches any alphanumeric character (including Hindi, etc.)
            # [^\w\s] matches any character that is NOT alphanumeric or space
            # We also strip underscores (_) which are included in \w by default
            message = re.sub(r'[^\w\s]|_', '', message)
            message = message.strip()
            lower_message = message.lower()

            session = ChatbotEngine._get_or_create_session(user, session_id)
            language = LanguageService.detect_language(message)

            if lower_message in ChatbotEngine.GREETINGS:
                reply = "Hello! I'm Vado from VaidyaGo. How can I help you today?"
                ChatbotEngine._save_message(session, "user", message, language)
                ChatbotEngine._save_message(session, "assistant", reply, language)
                return {
                    "reply": reply,
                    "session_id": session.id,
                    "intent": "chat",
                    "action": None,
                    "data": {},
                    "action_executed": False,
                }

            ChatbotEngine._save_message(session, "user", message, language)

            memory_context = MemoryService.get_memory_context(user=user, session=session)
            history = ChatbotEngine._build_history(session)

            prompt = PromptService.build_prompt(
                message=message,
                user=user,
                memory=memory_context,
                history=history,
            )

            llm_output = LLMService.generate_response(prompt)
            intent_data = IntentService.parse(llm_output)

            result = AgentManager.handle(intent_data, user)

            # Determine the final reply: 
            # Prioritize LLM's natural message if the action was executed successfully.
            # Otherwise, use the tool's result message (which might contain error info).
            if result.get("action_executed") and intent_data.get("message"):
                final_reply = intent_data.get("message")
            else:
                final_reply = result.get("message") or intent_data.get("message") or "I am here to help you."

            assistant_message = final_reply

            ChatbotEngine._save_message(session, "assistant", assistant_message, language)

            return {
                "reply": final_reply,
                "session_id": session.id,
                "intent": intent_data.get("intent", "chat"),
                "action": intent_data.get("action"),
                "data": result.get("data", {}),
                "action_executed": result.get("action_executed", False),
            }
        except Exception as e:
            logger.error(f"Chatbot Engine error: {str(e)}")
            return {
                "reply": "I'm sorry, I encountered a temporary issue while processing your request. Please try again in a moment.",
                "session_id": session_id,
                "intent": "chat",
                "action": None,
                "data": {},
                "action_executed": False,
            }

    @staticmethod
    def _get_or_create_session(user, session_id):
        if session_id:
            try:
                return ChatSession.objects.get(id=session_id, user=user)
            except ChatSession.DoesNotExist:
                pass
        return ChatSession.objects.create(user=user)

    @staticmethod
    def _build_history(session):
        messages = (
            ChatMessage.objects
            .filter(session=session)
            .order_by("-created_at")[:6]
        )
        return "\n".join([
            f"{msg.sender}: {msg.content}"
            for msg in reversed(messages)
        ])

    @staticmethod
    def _save_message(session, sender, content, language="en"):
        ChatMessage.objects.create(
            session=session,
            sender=sender,
            content=content,
            language=language,
        )
