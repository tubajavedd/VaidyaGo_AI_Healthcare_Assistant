import json
import logging
from chatbot_doctor.services.mistral_service import MistralService

logger = logging.getLogger(__name__)

class IntentService:
    @staticmethod
    def parse(llm_output):
        """
        Parses the LLM output into an intent and action.
        Expected format: {"intent": "...", "action": "...", "message": "...", "data": {...}}
        """
        try:
            # If the LLM output is already a JSON string
            if llm_output.strip().startswith("{"):
                return json.loads(llm_output)
            
            # If it's just plain text, wrap it as a chat intent
            return {
                "intent": "chat",
                "action": None,
                "message": llm_output,
                "data": {},
                "confidence": 1.0
            }
        except Exception as e:
            logger.error(f"Intent parsing error: {str(e)}")
            return {
                "intent": "chat",
                "action": None,
                "message": llm_output,
                "data": {},
                "confidence": 0.0
            }

    @staticmethod
    def extract_intent_with_llm(message, history, user=None, memory=""):
        """
        Use LLM to explicitly extract intent and data using PromptService.
        """
        from chatbot_doctor.services.prompt_service import PromptService
        prompt = PromptService.build_prompt(message, user, memory, history)
        
        # Pass full prompt with the required system prompt argument
        response = MistralService.generate_raw_response(prompt, "You are a medical admin assistant. Return valid JSON only.")
        
        if response:
            return IntentService.parse(response)
        return {"intent": "chat", "action": None, "message": "I'm not sure how to help with that specifically.", "data": {}}
