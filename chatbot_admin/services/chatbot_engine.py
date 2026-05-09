import logging
from chatbot_admin.models import AdminChatSession, AdminChatMessage
from chatbot_admin.services.language_service import detect_language
from chatbot_admin.services.memory_service import MemoryService
from chatbot_admin.services.intent_service import IntentService
from chatbot_admin.services.tool_router import ToolRouter

logger = logging.getLogger(__name__)

class ChatbotEngine:
    @staticmethod
    def process(user, message, session_id=None):
        message = message.strip()
        
        # 1. Session Management
        session = ChatbotEngine._get_or_create_session(user, session_id)
        language = detect_language(message)
        
        # 2. Save User Input
        AdminChatMessage.objects.create(session=session, sender="user", content=message, language=language)
        
        # 3. Context & Intent
        history = ChatbotEngine._build_history(session)
        intent_data = IntentService.extract_intent_with_llm(message, history)
        
        # 4. Action Execution
        action = intent_data.get("action")
        if action:
            result = ToolRouter.handle(action, intent_data.get("data", {}), user)
            final_reply = result.get("message")
            action_executed = result.get("action_executed", False)
            data = result.get("data", {})
        else:
            final_reply = intent_data.get("message")
            action_executed = False
            data = {}
            
        # 5. Save Response
        AdminChatMessage.objects.create(session=session, sender="assistant", content=final_reply, language=language)
        
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
