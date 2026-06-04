import json
import logging
from chatbot_admin.services.mistral_service import MistralService

logger = logging.getLogger(__name__)

class IntentService:
    @staticmethod
    def extract_intent_with_llm(message, history, user=None, memory_context=""):
        """
        Use LLM to explicitly extract intent and data using PromptService.
        """
        from chatbot_admin.services.prompt_service import PromptService
        prompt = PromptService.build_prompt(message, user, memory_context, history)
        
        # Pass full prompt with the required system prompt argument
        response = MistralService.generate_raw_response(prompt, "You are a platform admin assistant. Return valid JSON only.")
        
        if not response:
            return {"intent": "chat", "action": None, "message": "I'm not sure how to help with that specifically.", "data": {}}

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
