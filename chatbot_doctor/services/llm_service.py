import logging
from chatbot_doctor.services.mistral_service import MistralService
from chatbot_doctor.services.prompt_service import PromptService

logger = logging.getLogger(__name__)

class LLMService:
    @staticmethod
    def generate_response(prompt):
        """
        Generates a response using the preferred backend.
        """
        # Primary: Mistral
        response = MistralService.generate_response(prompt, PromptService.SYSTEM_PROMPT)
        
        if response:
            return response
            
        # Fallback: Simple message
        return "I'm sorry, I'm having trouble connecting to my brain right now. How else can I assist you, Doctor?"
