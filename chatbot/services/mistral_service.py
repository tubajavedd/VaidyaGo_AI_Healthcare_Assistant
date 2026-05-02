import json
import logging
import os
import requests
from chatbot.services.prompt_service import PromptService
from chatbot.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class MistralService:
    """
    LLM service wrapper for generating AI responses
    Uses LLMService for multi-backend support
    """

    @staticmethod
    def generate_response(user_message):
        """
        Generate AI response to user message using best available LLM backend
        """

        try:
            # Build the prompt
            prompt = PromptService.build_prompt(user_message)

            # Get response from LLM (tries multiple backends)
            llm_output = LLMService.generate_response(prompt)

            if not llm_output:
                return MistralService._create_error_response(
                    "Could not generate response from any available LLM backend"
                )

            logger.debug(f"LLM output: {llm_output[:200]}...")

            # Ensure response is in JSON format
            response_data = MistralService._ensure_json_response(llm_output)
            return response_data

        except Exception as e:
            logger.error(f"MistralService error: {str(e)}")
            return MistralService._create_error_response(str(e))

    @staticmethod
    def _ensure_json_response(text):
        """
        Ensure response is in valid JSON format
        """
        try:
            # Try to parse as JSON
            start = text.find("{")
            end = text.rfind("}") + 1

            if start >= 0 and end > start:
                json_str = text[start:end]
                data = json.loads(json_str)
                return json.dumps(data)  # Return as string
            else:
                # No JSON found, create response
                response = {
                    "intent": "chat",
                    "message": text,
                    "data": {}
                }
                return json.dumps(response)

        except json.JSONDecodeError:
            # Invalid JSON, wrap in response
            response = {
                "intent": "chat",
                "message": text,
                "data": {}
            }
            return json.dumps(response)
        except Exception as e:
            logger.error(f"Error ensuring JSON response: {str(e)}")
            return MistralService._create_error_response(f"Response parsing error: {str(e)}")

    @staticmethod
    def _create_error_response(error_message):
        """
        Create error response in JSON format
        """
        response = {
            "intent": "error",
            "message": error_message,
            "data": {
                "error": error_message
            }
        }
        return json.dumps(response)

