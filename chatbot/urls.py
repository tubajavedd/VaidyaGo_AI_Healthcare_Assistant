from django.urls import path
from chatbot.views import ChatAPIView

urlpatterns = [
    path("chat/", ChatAPIView.as_view(), name="chat"),
]
