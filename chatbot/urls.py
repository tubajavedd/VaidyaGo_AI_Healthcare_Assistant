from django.urls import path
from .views import chat_view, available_tools_view, tools_description_view

urlpatterns = [
    path("chat/", chat_view, name="chat"),
    path("tools/", available_tools_view, name="available_tools"),
    path("tools-description/", tools_description_view, name="tools_description"),
]

