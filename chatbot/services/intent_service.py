import json
import logging

logger = logging.getLogger(__name__)


class IntentService:
    """
    Parse LLM output to extract intent, action, message, and data.
    """

    @staticmethod
    def parse(llm_output):
        if isinstance(llm_output, dict):
            data = llm_output
        else:
            data = IntentService._extract_json(llm_output)

        return {
            "intent": data.get("intent", "chat"),
            "action": data.get("action"),
            "message": data.get("message", ""),
            "data": data.get("data", {}),
            "confidence": data.get("confidence", 0.5),
        }

    @staticmethod
    def _extract_json(text):
        if not isinstance(text, str):
            return {"intent": "chat", "message": str(text), "data": {}}

        start = text.find("{")
        end = text.rfind("}") + 1
        if start < 0 or end <= start:
            return {"intent": "chat", "message": text, "data": {}}

        try:
            payload = json.loads(text[start:end])
            return payload if isinstance(payload, dict) else {"intent": "chat", "message": text, "data": {}}
        except json.JSONDecodeError:
            try:
                cleaned = text[start:end].replace("\n", " ")
                return json.loads(cleaned)
            except Exception:
                return {"intent": "chat", "message": text, "data": {}}

