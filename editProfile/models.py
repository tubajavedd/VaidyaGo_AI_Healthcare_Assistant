from django.db import models
from django.conf import settings

# Create your models here.
class editProfile(models.Model):
    GENDER_CHOICES=[
        ("male","Male"),
        ("female","Female"),
        ("other","Other"),
    ]
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="edit_profile"
    )
    profile_photo=models.ImageField(
        upload_to="profile_photos/",
        null=True,
        blank=True
    )
    full_name=models.CharField(max_length=255)
    email=models.EmailField()

    phone_number=models.CharField(max_length=20)
    dob=models.DateField(
        null=True,
        blank=True
    )

    gender=models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="male"
    )

    residential_address=models.TextField()

    emergency_contact_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    emergency_contact_number = models.CharField(
    max_length=20,
    blank=True,
    null=True
    )


    created_at=models.DateTimeField(auto_now_add=True)
    update_st=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name