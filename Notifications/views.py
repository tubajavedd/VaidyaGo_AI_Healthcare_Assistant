from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Device, Notification
from .serializers import NotificationSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device(request):
    token = request.data.get("fcm_token")

    Device.objects.update_or_create(
        user=request.user,
        defaults={"fcm_token": token}
    )

    return Response({"message": "Device registered"})
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from Notifications.services.notifications_service import send_notification

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_notification(request):
    user = request.user
    phone = getattr(user, 'phone', None)

    send_notification(
        user=user,
        email=user.email,
        phone=phone
    )

    return Response({"message": "Notification sent successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)
