from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="chat_sessions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatSession {self.id} for {self.user or 'anonymous'}"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages"
    )
    sender = models.CharField(
        max_length=16,
        choices=(
            ("user", "user"),
            ("assistant", "assistant"),
        ),
        default="user"
    )
    content = models.TextField(default="", blank=True)
    language = models.CharField(max_length=10, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    # Compatibility fields for earlier chatbot data storage patterns
    user = models.CharField(max_length=100, blank=True, null=True, default="")
    message = models.TextField(default="", blank=True)
    response = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:60]}"
