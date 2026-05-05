import json
import logging
import os

from chatbot.services.tool_router import ToolRouter

logger = logging.getLogger(__name__)

#code
class AgentManager:
    """
    Multi-agent manager supporting both simple routing and AutoGen-based conversations.
    
    Can use:
    - Simple routing to ToolRouter (default)
    - AutoGen multi-agent framework (when enabled)
    """

    USE_AUTOGEN = os.getenv("CHATBOT_USE_AUTOGEN", "false").lower() == "true"

    @staticmethod
    def handle(intent_data, user):
        """
        Route intent to appropriate handler.
        """
        action = intent_data.get("action") or intent_data.get("intent")

        if not action or action == "chat":
            return {
                "message": intent_data.get("message", "I'm here to help."),
                "action_executed": False,
                "data": {},
            }

        if AgentManager.USE_AUTOGEN:
            try:
                return AgentManager._handle_with_autogen(intent_data, user)
            except Exception as e:
                logger.warning(f"AutoGen handling failed: {e}. Falling back to ToolRouter.")
                return ToolRouter.execute(intent_data, user)

        return ToolRouter.execute(intent_data, user)

    @staticmethod
    def _handle_with_autogen(intent_data, user):
        """
        Handle action using AutoGen multi-agent framework.
        """
        try:
            from autogen import AssistantAgent, UserProxyAgent
        except ImportError:
            logger.warning("AutoGen not available. Using ToolRouter.")
            return ToolRouter.execute(intent_data, user)

        action = intent_data.get("action")
        message = intent_data.get("message", "")
        data = intent_data.get("data", {})

        config_list = [
            {
                "model": os.getenv("MISTRAL_MODEL", "mistral-large"),
                "api_key": os.getenv("MISTRAL_API_KEY"),
                "base_url": "https://api.mistral.ai/v1",
            }
        ]

        assistant = AssistantAgent(
            name="Vado",
            system_message=(
                "You are Vado, a healthcare assistant for VaidyaGo. "
                "Help users with their healthcare requests. "
                "Be warm, friendly, and professional."
            ),
            llm_config={"config_list": config_list, "temperature": 0.7},
        )

        user_proxy = UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            code_execution_config=False,
        )

        task_prompt = f"Action: {action}\nData: {json.dumps(data)}\nMessage: {message}"

        try:
            user_proxy.initiate_chat(assistant, message=task_prompt)
            response_text = user_proxy.last_message()
            return {
                "message": response_text.get("content", message) if isinstance(response_text, dict) else str(response_text),
                "action_executed": True,
                "data": data,
            }
        except Exception as e:
            logger.error(f"AutoGen conversation failed: {e}")
            raise

    @staticmethod
    def get_autogen_status():
        """
        Get current AutoGen status and configuration.
        """
        return {
            "autogen_enabled": AgentManager.USE_AUTOGEN,
            "autogen_available": AgentManager._is_autogen_available(),
            "mistral_api_key_set": bool(os.getenv("MISTRAL_API_KEY")),
            "mistral_model": os.getenv("MISTRAL_MODEL", "mistral-large"),
        }

    @staticmethod
    def _is_autogen_available():
        """
        Check if AutoGen is available.
        """
        try:
            import autogen
            return True
        except ImportError:
            return False
