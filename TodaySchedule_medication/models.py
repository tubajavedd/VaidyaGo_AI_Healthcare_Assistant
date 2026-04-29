from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Schedule(models.Model):
    ROUTINE_CHOICES = (
        ('Routine', 'Routine'),
        ('As Needed', 'As Needed'),
    )

    FREQUENCY_CHOICES = (
        ('Once Daily', 'Once Daily'),
        ('Twice Daily', 'Twice Daily'),
        ('Thrice Daily', 'Thrice Daily'),
        ('Every 4 Hours', 'Every 4 Hours'),
        ('Every 6 Hours', 'Every 6 Hours'),
        ('Every 8 Hours', 'Every 8 Hours'),
        ('Every 12 Hours', 'Every 12 Hours'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schedules'
    )

    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES
    )
    time = models.TimeField()
    routine_type = models.CharField(
        max_length=20,
        choices=ROUTINE_CHOICES
    )

    date = models.DateField(auto_now_add=True)

    is_taken = models.BooleanField(default=False)
    taken_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medication_name