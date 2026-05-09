import json
import logging
from chatbot_admin.services.mistral_service import MistralService

logger = logging.getLogger(__name__)

class IntentService:
    @staticmethod
    def extract_intent_with_llm(message, history):
        system_prompt = """
        You are a platform admin intent extractor. Analyze the administrator's message and return a JSON object.
        Available Actions:
        - dashboard_summary (params: none) - Use this for 'analyze dashboard', 'how is the platform', 'overall status', etc.
        - doctor_management (params: filter, action, doctor_id)
        - doctor_approval (params: doctor_id, action)
        - patient_management (params: filter, action, patient_id)
        - appointments_management (params: filter, action, appointment_id)
        - slot_management (params: action)
        - revenue_analytics (params: period)
        - user_analytics (params: none)
        - notifications (params: target, message)
        - support_tickets (params: action, ticket_id)
        - system_health (params: none)
        - security (params: action)
        - reports (params: report_type)
        - maintenance (params: action)
        - logs (params: category)
        - ai_analytics (params: none)
        - chat (no action)

        Return format: {"intent": "string", "action": "string or null", "message": "conversational response", "data": {}}
        """
        prompt = f"History: {history}\nMessage: {message}"
        response = MistralService.generate_raw_response(prompt, system_prompt)
        response_text = response.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        try:
            if response_text.startswith("{"):
                return json.loads(response_text)
            return {
                "intent": "chat",
                "action": None,
                "message": response,
                "data": {}
            }
        except Exception:
            return {"intent": "chat", "action": None, "message": response, "data": {}}
