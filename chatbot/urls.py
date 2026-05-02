from django.urls import path
<<<<<<< HEAD
from .views import chat_view, available_tools_view, tools_description_view

urlpatterns = [
    path("chat/", chat_view, name="chat"),
    path("tools/", available_tools_view, name="available_tools"),
    path("tools-description/", tools_description_view, name="tools_description"),
]

=======
from chatbot.views import ChatAPIView

urlpatterns = [
    path("chat/", ChatAPIView.as_view(), name="chat"),
]
>>>>>>> 53e8d66e4be476e111c5aaf60c4a70bb6e1a1cff
