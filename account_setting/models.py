from django.db import models
from django.conf import settings


class AccountSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account_settings"
    )

    # Account details
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    clinician_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    # Preferences
    language = models.CharField(
        max_length=100,
        default="English (United Kingdom)"
    )
    timezone = models.CharField(
        max_length=100,
        default="GMT +05:30 (Mumbai, India)"
    )
    automatic_updates = models.BooleanField(default=True)

    # Security
    two_factor_enabled = models.BooleanField(default=False)

    # Privacy
    data_sharing = models.BooleanField(default=False)
    profile_visibility = models.CharField(
        max_length=50,
        default="internal_only"
    )
    hipaa_logs_enabled = models.BooleanField(default=True)

    # Critical actions
    account_deactivated = models.BooleanField(default=False)
    request_data_deletion = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
