from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Device

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device(request):
    token = request.data.get("fcm_token")

    Device.objects.update_or_create(
        user=request.user,
        defaults={"fcm_token": token}
    )

    return Response({"message": "Device registered"})
