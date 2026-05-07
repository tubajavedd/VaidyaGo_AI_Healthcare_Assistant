"""
LLM Service wrapper that prefers Mistral API and falls back to simple local extraction logic.
"""

import json
import logging
import random

from chatbot.services.mistral_service import MistralService
from chatbot.services.smart_extractor import SmartIntentExtractor
from chatbot.services.vaidyago_knowledge_base import VaidyaGoKnowledge

logger = logging.getLogger(__name__)

INTERJECTIONS = {
    "positive": ["🤩 ", "✨ ", "🌟 ", "✅ ", "👏 ", "🔥 ", "🚀 ", "🎯 "],
    "relief": ["🎉 ", "🎊 ", "🙌 ", "🥳 ", "🎈 ", "🥂 "],
    "surprise": ["🤯 ", "😲 ", "😮 ", "💥 ", "⚡ ", "⁉️ "],
    "negative": ["😟 ", "😔 ", "🆘 ", "❌ ", "⚠️ ", "🩹 "],
    "emotional": ["🥺 ", "❤️ ", "💖 ", "🙏 ", "🌈 ", "🌻 ", "🫂 "]
}

INTENT_EMOTION_MAP = {
    "book_appointment": "relief",
    "cancel_appointment": "negative",
    "emergency": "negative",
    "get_prescriptions": "positive",
    "get_notifications": "positive",
    "reschedule_appointment": "relief",
    "chat": "positive",
    "get_doctor_slots": "positive"
}

HEALTH_QUOTES = [
    "Health is the greatest wealth.",
    "A healthy outside starts from the inside.",
    "Take care of your body. It's the only place you have to live.",
    "Happiness is the highest form of health.",
    "Keep your vitality. A life without health is like a river without water.",
]

class LLMService:
    """
    Central LLM service with Mistral API as primary backend.
    Falls back to knowledge base for VaidyaGo questions, then to local extraction.
    """

    BACKENDS = ["mistral", "knowledge", "fallback"]

    @staticmethod
    def _add_personality(response_json: str) -> str:
        """
        Injects enthusiasm and quotes into the conversational message based on intent.
        """
        try:
            data = json.loads(response_json)
            message = data.get("message", "")
            intent = data.get("intent", "chat")
            
            # Determine emotion category based on intent
            emotion_category = INTENT_EMOTION_MAP.get(intent, "positive")
            
            # Add prefix sometimes
            if random.random() < 0.4:
                prefix = random.choice(INTERJECTIONS.get(emotion_category, INTERJECTIONS["positive"]))
                # Check if message already starts with an interjection to avoid "Wow! Wow!"
                if not any(message.startswith(p.strip()) for cat in INTERJECTIONS.values() for p in cat):
                    message = prefix + message
            
            # Add quote sometimes
            if random.random() < 0.2:
                message += f"\n\n💡 Remember: \"{random.choice(HEALTH_QUOTES)}\""
            
            data["message"] = message
            return json.dumps(data)
        except Exception:
            return response_json

    @staticmethod
    def generate_response(prompt: str) -> str:
        logger.info("Attempting to generate LLM response")

        for backend in LLMService.BACKENDS:
            try:
                logger.debug(f"Trying backend: {backend}")

                if backend == "mistral":
                    result = MistralService.generate_response(prompt)
                elif backend == "knowledge":
                    result = LLMService._try_knowledge_base(prompt)
                elif backend == "fallback":
                    result = LLMService._try_fallback(prompt)
                else:
                    result = None

                if result:
                    logger.info(f"Success using {backend}")
                    return LLMService._add_personality(result)

            except Exception as e:
                logger.warning(f"{backend} failed: {str(e)}")
                continue

        logger.warning("All backends failed. Using fallback response")
        return LLMService._add_personality(LLMService._try_fallback(prompt))

    @staticmethod
    def _try_knowledge_base(prompt: str) -> str:
        """
        Check VaidyaGo knowledge base for answers to platform questions.
        """
        try:
            message_start = prompt.find("--- USER MESSAGE ---")
            if message_start != -1:
                parts = prompt[message_start:].split("\n")
                message_part = parts[1].strip() if len(parts) > 1 else prompt
            else:
                message_part = prompt

            answer = VaidyaGoKnowledge.get_answer(message_part)
            
            if answer:
                return json.dumps({
                    "intent": "chat",
                    "action": None,
                    "message": answer,
                    "data": {},
                    "confidence": 0.95,
                })

            return None

        except Exception as e:
            logger.debug(f"Knowledge base lookup failed: {str(e)}")
            return None

    @staticmethod
    def _try_fallback(prompt: str) -> str:
        try:
            message_start = prompt.find("--- USER MESSAGE ---")
            if message_start != -1:
                parts = prompt[message_start:].split("\n")
                message_part = parts[1].strip() if len(parts) > 1 else prompt
            else:
                message_part = prompt

            lower_msg = message_part.lower()
            intent = "chat"
            action = None
            response_message = "I'm here to help you."
            data = {}

            # 1. Check knowledge base directly with the refined keyword map
            knowledge_answer = VaidyaGoKnowledge.get_answer(lower_msg)
            if knowledge_answer:
                # Priority for emergency intent
                if any(term in lower_msg for term in ["chest pain", "breathe", "emergency", "heart attack", "unconscious", "bleeding"]):
                    intent = "emergency"
                
                return json.dumps({
                    "intent": intent,
                    "action": None,
                    "message": knowledge_answer,
                    "data": {},
                    "confidence": 0.9,
                })

            # 2. Check for action-triggering logic (Booking, Cancellation, etc.)
            if any(phrase in lower_msg for phrase in ["how book", "how to book", "book appointment", "schedule appointment", "book a slot", "bok apointment"]):
                intent = "book_appointment"
                action = "book_appointment"
                extracted = SmartIntentExtractor.extract_appointment_details(message_part)
                data = {k: v for k, v in extracted.items() if v is not None}
                booking_response = SmartIntentExtractor.build_booking_response(message_part, extracted)
                response_message = booking_response.get("message", response_message)
                data = booking_response.get("extracted", data)

            elif any(word in lower_msg for word in ["book appointment", "schedule appointment", "book a slot", "appointment"]):
                intent = "book_appointment"
                action = "book_appointment"
                extracted = SmartIntentExtractor.extract_appointment_details(message_part)
                data = {k: v for k, v in extracted.items() if v is not None}
                booking_response = SmartIntentExtractor.build_booking_response(message_part, extracted)
                response_message = booking_response.get("message", response_message)
                data = booking_response.get("extracted", data)

            elif any(phrase in lower_msg for phrase in ["cancel appointment", "how cancel", "delete appointment", "cncl"]):
                intent = "cancel_appointment"
                action = "cancel_appointment"
                response_message = "I can help cancel your appointment. Please provide the appointment ID."

            elif "reschedule" in lower_msg and "appointment" in lower_msg:
                intent = "reschedule_appointment"
                action = "reschedule_appointment"
                response_message = "I can help reschedule your appointment. Please provide the appointment ID, new date, and time."

            elif any(phrase in lower_msg for phrase in ["find doctor", "doctor slots", "available slot", "slots"]):
                intent = "get_doctor_slots"
                action = "get_doctor_slots"
                response_message = "I can check doctor availability. Please share the doctor name and desired date."

            elif any(phrase in lower_msg for phrase in ["prescription", "medicine", "medication", "my prescriptions"]):
                intent = "get_prescriptions"
                action = "get_prescriptions"
                response_message = "I can fetch your prescriptions for you."

            elif "notification" in lower_msg:
                intent = "get_notifications"
                action = "get_notifications"
                response_message = "I can pull your latest notifications."

            return json.dumps({
                "intent": intent,
                "action": action,
                "message": response_message,
                "data": data,
                "confidence": 0.8 if action else 0.85,
            })

        except Exception as exc:
            logger.error(f"Fallback parse failed: {str(exc)}")
            return json.dumps({
                "intent": "chat",
                "action": None,
                "message": "I am here to help you with VaidyaGo. You can ask me about booking appointments, managing healthcare, or anything about the platform.",
                "data": {},
                "confidence": 0.0,
            })
