from django.db import models

class ChatMessage(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True, default='')
    message = models.TextField(default='', blank=True)
    response = models.TextField(default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
