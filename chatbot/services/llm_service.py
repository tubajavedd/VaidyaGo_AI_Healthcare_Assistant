"""
LLM Service with multiple backend support
- Local TinyLlama model
- HuggingFace API
- OpenAI API
- Fallback JSON mode
"""

import json
import logging
import os
import requests

from chatbot.services.smart_extractor import SmartIntentExtractor

logger = logging.getLogger(__name__)


class LLMService:
    """
    Central LLM service with multiple backend support
    """

    BACKENDS = ["local", "openai", "huggingface", "fallback"]

    @staticmethod
    def generate_response(prompt: str) -> str:
        """
        Generate response using best available backend
        """
        logger.info("Attempting to generate LLM response")

        for backend in LLMService.BACKENDS:
            try:
                logger.debug(f"Trying backend: {backend}")

                if backend == "local":
                    result = LLMService._try_local_llm(prompt)

                elif backend == "openai":
                    result = LLMService._try_openai(prompt)

                elif backend == "huggingface":
                    result = LLMService._try_huggingface(prompt)

                elif backend == "fallback":
                    result = LLMService._try_fallback(prompt)

                else:
                    result = None

                if result and not result.startswith("Error:"):
                    logger.info(f"Success using {backend}")
                    return result

            except Exception as e:
                logger.warning(f"{backend} failed: {str(e)}")
                continue

        logger.warning("All backends failed. Using fallback.")
        return LLMService._try_fallback(prompt)

    @staticmethod
    def _try_local_llm(prompt: str):
        """
        Try local TinyLlama
        """
        try:
            from transformers import pipeline

            pipe = pipeline(
                "text-generation",
                model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                device=-1
            )

            result = pipe(
                prompt,
                max_new_tokens=300,
                temperature=0.7,
                do_sample=True,
                top_p=0.95
            )

            if result:
                return result[0].get("generated_text", "").strip()

            return None

        except Exception as e:
            logger.debug(f"Local LLM failed: {str(e)}")
            return None

    @staticmethod
    def _try_openai(prompt: str):
        """
        Try OpenAI API
        """
        try:
            import openai

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return None

            openai.api_key = api_key

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
                timeout=30
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.debug(f"OpenAI failed: {str(e)}")
            return None

    @staticmethod
    def _try_huggingface(prompt: str):
        """
        Try HuggingFace API
        """
        try:
            api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
            hf_api_key = os.getenv("HF_API_KEY")

            if not hf_api_key:
                return None

            headers = {
                "Authorization": f"Bearer {hf_api_key}"
            }

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.7
                }
            }

            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30,
                proxies={"http": None, "https": None}
            )

            if response.status_code == 200:
                data = response.json()

                if isinstance(data, list) and data:
                    return data[0].get("generated_text", "").strip()

                if isinstance(data, dict):
                    return data.get("generated_text", "").strip()

            logger.warning(
                f"HuggingFace API error {response.status_code}: {response.text}"
            )
            return None

        except Exception as e:
            logger.debug(f"HuggingFace failed: {str(e)}")
            return None

    @staticmethod
    def _try_fallback(prompt: str):
        """
        Simple fallback logic without LLM
        """
        try:
            message_start = prompt.find("--- USER MESSAGE ---")

            if message_start != -1:
                parts = prompt[message_start:].split("\n")
                if len(parts) > 1:
                    message_part = parts[1].strip()
                else:
                    message_part = prompt[-200:] if len(prompt) > 200 else prompt
            else:
                message_part = prompt[-200:] if len(prompt) > 200 else prompt

            lower_msg = message_part.lower()

            intent = "chat"
            action = None
            message = "I'm here to help you."

            data = {}

            if any(word in lower_msg for word in ["book", "appointment", "schedule"]):
                intent = "book_appointment"
                action = "book_appointment"

                extracted = SmartIntentExtractor.extract_appointment_details(
                    message_part
                )

                data = {k: v for k, v in extracted.items() if v is not None}

                booking_response = SmartIntentExtractor.build_booking_response(
                    message_part,
                    extracted
                )

                message = booking_response["message"]
                data = booking_response.get("extracted", {})

            elif "cancel" in lower_msg and "appointment" in lower_msg:
                intent = "cancel_appointment"
                action = "cancel_appointment"
                message = "Please provide appointment ID to cancel."

            elif "slot" in lower_msg or "available" in lower_msg:
                intent = "get_doctor_slots"
                action = "get_doctor_slots"
                message = "Please provide doctor ID and date."

            elif "prescription" in lower_msg or "medicine" in lower_msg:
                intent = "prescriptions"
                action = "get_prescriptions"
                message = "Fetching prescriptions."

            elif "notification" in lower_msg:
                intent = "notifications"
                action = "get_notifications"
                message = "Fetching notifications."

            response = {
                "intent": intent,
                "action": action,
                "message": message,
                "data": data,
                "confidence": 0.7
            }

            logger.info(f"Fallback detected intent: {intent}")
            return json.dumps(response)

        except Exception as e:
            logger.error(f"Fallback error: {str(e)}")

            return json.dumps({
                "intent": "chat",
                "action": None,
                "message": "Hello, I'm Vado. How may I help you?",
                "data": {},
                "confidence": 0.5
            })
