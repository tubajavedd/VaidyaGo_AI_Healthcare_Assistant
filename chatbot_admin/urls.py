from django.urls import path
from chatbot_admin.views import platform_admin_chat_view, platform_admin_tools_view

urlpatterns = [
    path("chat/", platform_admin_chat_view, name="platform-admin-chat"),
    path("tools/", platform_admin_tools_view, name="platform-admin-tools"),
]
