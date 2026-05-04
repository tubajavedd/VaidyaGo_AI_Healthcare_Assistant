import json
import logging
import os
import requests

from chatbot.services.prompt_service import PromptService

logger = logging.getLogger(__name__)


class MistralService:
    """
    Wrapper for the Mistral API.
    """

    @staticmethod
    def generate_response(prompt: str) -> str:
        api_key = os.getenv("MISTRAL_API_KEY")
        model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

        if not api_key:
            logger.warning("MISTRAL_API_KEY is not configured")
            return None

        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": PromptService.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512,
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, dict):
                choices = result.get("choices") or []
                if choices:
                    assistant_message = choices[0].get("message", {}).get("content")
                    if assistant_message:
                        return assistant_message.strip()

            logger.warning("Unexpected Mistral response structure")
            return None

        except requests.RequestException as exc:
            logger.error(f"Mistral API request failed: {exc}")
            return None
        except (json.JSONDecodeError, KeyError) as exc:
            logger.error(f"Mistral response parsing failed: {exc}")
            return None

