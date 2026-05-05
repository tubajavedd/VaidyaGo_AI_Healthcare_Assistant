from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReminderViewSet, FCMTokenRegisterView

router = DefaultRouter()
router.register(r'', ReminderViewSet, basename='reminder')

urlpatterns = [
    path('fcm/register/', FCMTokenRegisterView.as_view(), name='fcm-register'),
    path('reminders/', include(router.urls)),
]
