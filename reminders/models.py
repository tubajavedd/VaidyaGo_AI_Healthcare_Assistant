from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

class Reminder(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    medicine = models.CharField(max_length=200)
    time = models.TimeField()              # base time of day (e.g., 08:00)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='once')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)      # optional stop date
    next_reminder_datetime = models.DateTimeField(editable=False, null=True, blank=True)  # computed
    is_active = models.BooleanField(default=True)
    snooze_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.next_reminder_datetime:
            self.next_reminder_datetime = self.compute_next_datetime()
        super().save(*args, **kwargs)

    def compute_next_datetime(self):
        """Combine start_date + time, then apply frequency logic"""
        # A simple implementation for the next occurrence
        now = timezone.now()
        base_datetime = timezone.make_aware(datetime.combine(self.start_date, self.time))
        
        if self.frequency == 'once':
            return base_datetime if base_datetime > now else None
            
        next_dt = base_datetime
        while next_dt <= now:
            if self.frequency == 'daily':
                next_dt += timedelta(days=1)
            elif self.frequency == 'weekly':
                next_dt += timedelta(weeks=1)
            elif self.frequency == 'monthly':
                # rough approximation, typically use dateutil.relativedelta
                next_dt += timedelta(days=30)
                
        if self.end_date:
            end_datetime = timezone.make_aware(datetime.combine(self.end_date, datetime.max.time()))
            if next_dt > end_datetime:
                return None
                
        return next_dt

class FCMToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
