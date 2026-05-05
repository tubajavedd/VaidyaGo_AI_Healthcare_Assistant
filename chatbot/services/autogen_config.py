"""
AutoGen Configuration Helper for VaidyaGo Chatbot.

This module provides AutoGen setup and utilities for multi-agent healthcare conversations.

Usage:
    1. Set environment variables:
       - CHATBOT_USE_AUTOGEN=true
       - MISTRAL_API_KEY=your_api_key
       - MISTRAL_MODEL=mistral-large (optional)

    2. Import and use:
       from chatbot.services.autogen_config import get_autogen_config
       config = get_autogen_config()
"""

import json
import logging
import os

logger = logging.getLogger(__name__)


def get_autogen_config():
    """
    Get AutoGen LLM configuration for Mistral API.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    model = os.getenv("MISTRAL_MODEL", "mistral-large")

    if not api_key:
        logger.warning("MISTRAL_API_KEY not configured for AutoGen")
        return None

    return [
        {
            "model": model,
            "api_key": api_key,
            "base_url": "https://api.mistral.ai/v1",
        }
    ]


def get_healthcare_assistant_config():
    """
    Get AutoGen assistant configuration for healthcare context.
    """
    return {
        "name": "Vado",
        "system_message": (
            "You are Vado, the friendly healthcare assistant for VaidyaGo. "
            "Help users with healthcare queries, appointment management, and medical information. "
            "Be warm, empathetic, and professional. "
            "Do not provide medical diagnosis. Always recommend consulting a healthcare provider when needed."
        ),
        "llm_config": {
            "config_list": get_autogen_config() or [],
            "temperature": 0.7,
            "max_tokens": 512,
        },
    }


def enable_autogen():
    """
    Enable AutoGen mode in the chatbot.
    """
    os.environ["CHATBOT_USE_AUTOGEN"] = "true"
    logger.info("AutoGen enabled for chatbot")


def disable_autogen():
    """
    Disable AutoGen mode in the chatbot.
    """
    os.environ["CHATBOT_USE_AUTOGEN"] = "false"
    logger.info("AutoGen disabled for chatbot")


def is_autogen_enabled():
    """
    Check if AutoGen is enabled.
    """
    return os.getenv("CHATBOT_USE_AUTOGEN", "false").lower() == "true"


def validate_autogen_setup():
    """
    Validate AutoGen setup and requirements.
    
    Returns dict with status and any issues found.
    """
    issues = []

    try:
        import autogen
        logger.info(f"AutoGen installed: {autogen.__version__}")
    except ImportError:
        issues.append("AutoGen (pyautogen) not installed")

    if not os.getenv("MISTRAL_API_KEY"):
        issues.append("MISTRAL_API_KEY environment variable not set")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "autogen_enabled": is_autogen_enabled(),
        "mistral_configured": bool(os.getenv("MISTRAL_API_KEY")),
    }
