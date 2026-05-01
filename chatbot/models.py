from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.title}"


class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    )

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    language = models.CharField(max_length=20, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"


class UserMemory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="memories"
    )
    key = models.CharField(max_length=255)
    value = models.TextField()
    confidence_score = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "key")

    def __str__(self):
        return f"{self.key}: {self.value}"
