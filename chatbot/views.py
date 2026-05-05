import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.chatbot_engine import ChatbotEngine
from .services.tool_router import ToolRouter
from .services.tools_registry import ToolsRegistry
from .serializers import ChatRequestSerializer, ChatResponseSerializer

logger = logging.getLogger(__name__)


@api_view(["POST"])
def chat_view(request):
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": "Invalid request payload",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    message = serializer.validated_data["message"].strip()
    session_id = serializer.validated_data.get("session_id")
    user = request.user if request.user and request.user.is_authenticated else None

    response_data = ChatbotEngine.process(
        user=user,
        message=message,
        session_id=session_id,
    )

    response_serializer = ChatResponseSerializer(data=response_data)
    if not response_serializer.is_valid():
        logger.error(f"Chat response serialization failed: {response_serializer.errors}")
        return Response(
            {
                "success": False,
                "error": "Unable to build chatbot response",
                "details": response_serializer.errors,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {
            "success": True,
            **response_serializer.validated_data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def available_tools_view(request):
    try:
        category = request.query_params.get("category")
        tools = ToolRouter.get_available_tools(category)

        return Response(
            {
                "success": True,
                "tools": tools,
                "categories": ToolsRegistry.get_categories(),
            }
        )
    except Exception as e:
        logger.error(f"Error in available_tools_view: {str(e)}")
        return Response(
            {
                "success": False,
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def tools_description_view(request):
    try:
        summary = ToolsRegistry.get_tools_summary()

        return Response(
            {
                "success": True,
                "tools": summary,
                "total_tools": len(ToolsRegistry.get_all_tools()),
                "categories": ToolsRegistry.get_categories(),
            }
        )
    except Exception as e:
        logger.error(f"Error in tools_description_view: {str(e)}")
        return Response(
            {
                "success": False,
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

