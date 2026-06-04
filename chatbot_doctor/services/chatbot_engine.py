import logging
from chatbot_doctor.models import AdminChatSession, AdminChatMessage
from chatbot_doctor.services.language_service import detect_language
from chatbot_doctor.services.memory_service import MemoryService
from chatbot_doctor.services.prompt_service import PromptService
from chatbot_doctor.services.llm_service import LLMService
from chatbot_doctor.services.intent_service import IntentService
from chatbot_doctor.services.tool_router import ToolRouter

logger = logging.getLogger(__name__)

class ChatbotEngine:
    @staticmethod
    def process(user, message, session_id=None):
        if isinstance(message, dict):
            message = message.get('text') or message.get('message') or str(message)
        elif message is None:
            message = ''
        else:
            message = str(message)
        message = message.strip()
        
        # 1. Get or create session
        session = ChatbotEngine._get_or_create_session(user, session_id)
        language = detect_language(message)
        
        # 2. Save user message
        ChatbotEngine._save_message(session, "user", message, language)
        
        # 3. Build context
        memory_context = MemoryService.get_memory_context(user, session)
        history = ChatbotEngine._build_history(session)
        
        # 4. Extract intent and data
        intent_data = IntentService.extract_intent_with_llm(message, history, user, memory_context)
        
        # 5. Handle tools
        action = intent_data.get("action")
        if action:
            result = ToolRouter.handle(action, intent_data.get("data", {}), user)
            final_reply = result.get("message")
            action_executed = result.get("action_executed", False)
            data = result.get("data", {})
        else:
            final_reply = intent_data.get("message") or "I'm sorry, I couldn't process that request."
            action_executed = False
            data = {}
            
        # 6. Save assistant response
        ChatbotEngine._save_message(session, "assistant", final_reply, language)
        
        return {
            "reply": final_reply,
            "session_id": session.id,
            "intent": intent_data.get("intent", "chat"),
            "action": action,
            "data": data,
            "action_executed": action_executed,
        }

    @staticmethod
    def _get_or_create_session(user, session_id):
        if session_id:
            try:
                return AdminChatSession.objects.get(id=session_id, user=user)
            except AdminChatSession.DoesNotExist:
                pass
        return AdminChatSession.objects.create(user=user)

    @staticmethod
    def _build_history(session):
        messages = AdminChatMessage.objects.filter(session=session).order_by("-created_at")[:6]
        return "\n".join([f"{m.sender}: {m.content}" for m in reversed(messages)])

    @staticmethod
    def _save_message(session, sender, content, language="en"):
        AdminChatMessage.objects.create(
            session=session,
            sender=sender,
            content=content,
            language=language
        )
