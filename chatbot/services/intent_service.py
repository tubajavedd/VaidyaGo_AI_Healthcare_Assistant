import json
import logging

logger = logging.getLogger(__name__)


class IntentService:
    """
    Parse LLM output to extract intent and action
    """

    @staticmethod
    def parse(mistral_output):
        """
        Parse LLM response and extract intent, action, message, and data
        """

        try:
            # If mistral_output is already a string, try to parse it
            if isinstance(mistral_output, str):
                # Extract JSON from response
                start = mistral_output.find("{")
                end = mistral_output.rfind("}") + 1

                if start >= 0 and end > start:
                    json_str = mistral_output[start:end]
                    data = json.loads(json_str)
                else:
                    # No JSON found
                    data = {
                        "intent": "chat",
                        "message": mistral_output,
                        "data": {}
                    }
            else:
                data = mistral_output

            # Validate and ensure required fields
            intent_data = {
                "intent": data.get("intent", "chat"),
                "action": data.get("action"),
                "message": data.get("message", ""),
                "data": data.get("data", {}),
                "confidence": data.get("confidence", 0.5)
            }

            logger.debug(f"Parsed intent: {intent_data['intent']}, action: {intent_data['action']}")
            return intent_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            return {
                "intent": "chat",
                "action": None,
                "message": mistral_output if isinstance(mistral_output, str) else str(mistral_output),
                "data": {},
                "confidence": 0.0
            }
        except Exception as e:
            logger.error(f"Error parsing intent: {str(e)}")
            return {
                "intent": "chat",
                "action": None,
                "message": "I encountered an error processing your request.",
                "data": {},
                "confidence": 0.0
            }

