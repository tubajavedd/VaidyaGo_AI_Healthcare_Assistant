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

        # Merge 'parameters' into 'data' if 'data' is empty and 'parameters' exists
        # This handles cases where LLM uses 'parameters' instead of 'data'
        intent_data = data.get("data", {})
        if not intent_data and "parameters" in data:
            intent_data = data.get("parameters", {})

        return {
            "intent": data.get("intent", "chat"),
            "action": data.get("action"),
            "message": data.get("message", ""),
            "data": intent_data,
            "confidence": data.get("confidence", 0.5),
        }

    @staticmethod
    def _extract_json(text):
        if not isinstance(text, str):
            return {"intent": "chat", "message": str(text), "data": {}}

        # 1. Clean up markdown code blocks if present
        cleaned_text = text.strip()
        if cleaned_text.startswith("```"):
            # Remove start/end block markers
            import re
            cleaned_text = re.sub(r'^```[a-z]*\n', '', cleaned_text)
            cleaned_text = re.sub(r'\n```$', '', cleaned_text)
            cleaned_text = cleaned_text.strip()

        start = cleaned_text.find("{")
        end = cleaned_text.rfind("}") + 1
        
        if start < 0 or end <= start:
            return {"intent": "chat", "message": text, "data": {}}

        json_str = cleaned_text[start:end]

        # 2. Fix common LLM mistakes
        import re
        # Only remove plus signs that are between quotes (concatenation)
        json_str = re.sub(r'"\s*\+\s*"', '', json_str)
        # Remove single-line comments (//...) but avoid stripping URLs (://)
        json_str = re.sub(r'(?m)(?<!:)\s*//.*$', '', json_str)

        try:
            payload = json.loads(json_str)
            return payload if isinstance(payload, dict) else {"intent": "chat", "message": text, "data": {}}
        except json.JSONDecodeError:
            try:
                # Last resort: remove literal newlines inside strings or trailing commas
                # This is a bit aggressive but helps with typical LLM messes
                cleaned = json_str.replace("\n", " ").replace("\r", " ")
                return json.loads(cleaned)
            except Exception:
                return {"intent": "chat", "message": text, "data": {}}

