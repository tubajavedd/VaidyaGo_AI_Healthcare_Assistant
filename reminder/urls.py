# reminders/urls.py
from django.urls import path
from .views import create_reminder, snooze_reminder, dismiss_reminder, list_reminders, update_reminder

urlpatterns = [
    path('', list_reminders),
    path('create/', create_reminder),
    path('<int:id>/snooze/', snooze_reminder),
    path('<int:id>/dismiss/', dismiss_reminder),
    path('<int:id>/update/', update_reminder),
]
