import json
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.mistral_service import MistralService
from .services.intent_service import IntentService
from .services.tool_router import ToolRouter
from .services.tools_registry import ToolsRegistry
from .models import ChatMessage

logger = logging.getLogger(__name__)


@api_view(["POST"])
def chat_view(request):
    """
    Main chatbot endpoint
    Receives user message, processes with LLM, and executes appropriate action
    """

    try:
        # Get user message from request
        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response(
                {
                    "error": "Message is required",
                    "message": "Please provide a message"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user if request.user and request.user.is_authenticated else None

        logger.info(f"Processing message from {user}: {user_message[:100]}")

        # 1. Generate LLM response
        llm_output = MistralService.generate_response(user_message)

        # 2. Parse intent and extract action
        intent_data = IntentService.parse(llm_output)

        # 3. Execute tool/action if specified
        result = ToolRouter.execute(intent_data, user)

        # 4. Store conversation in database (if user is authenticated)
        if user:
            try:
                ChatMessage.objects.create(
                    user=user.username,
                    message=user_message,
                    response=result.get("message", "")
                )
            except Exception as e:
                logger.warning(f"Failed to store chat message: {str(e)}")

        # 5. Return response
        return Response(
            {
                "success": True,
                "message": result.get("message", ""),
                "intent": intent_data.get("intent"),
                "action": intent_data.get("action"),
                "data": result.get("data"),
                "action_executed": result.get("action_executed", False)
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Error in chat_view: {str(e)}")
        return Response(
            {
                "success": False,
                "error": str(e),
                "message": "An error occurred processing your request"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def available_tools_view(request):
    """
    Get list of available tools/actions for the chatbot
    """
    try:
        category = request.query_params.get("category")
        tools = ToolRouter.get_available_tools(category)
        
        return Response(
            {
                "success": True,
                "tools": tools,
                "categories": ToolsRegistry.get_categories()
            }
        )
    except Exception as e:
        logger.error(f"Error in available_tools_view: {str(e)}")
        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def tools_description_view(request):
    """
    Get detailed description of all available tools
    """
    try:
        summary = ToolsRegistry.get_tools_summary()
        
        return Response(
            {
                "success": True,
                "tools": summary,
                "total_tools": len(ToolsRegistry.get_all_tools()),
                "categories": ToolsRegistry.get_categories()
            }
        )
    except Exception as e:
        logger.error(f"Error in tools_description_view: {str(e)}")
        return Response(
            {
                "success": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

