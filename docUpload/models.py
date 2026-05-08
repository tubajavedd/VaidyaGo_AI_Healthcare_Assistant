from django.db import models
from django.conf import settings
import hashlib
# Create your models here.

def upload_path(instance,filename):
    return f"document/user_{instance.user.id}/{filename}"

class userDoc(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    file=models.FileField(upload_to=upload_path)
    file_hash=models.CharField(max_length=64,unique=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title