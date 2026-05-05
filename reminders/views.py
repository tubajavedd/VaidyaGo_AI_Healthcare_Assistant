from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import Reminder, FCMToken
from .serializers import ReminderSerializer, FCMTokenSerializer

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.filter(is_active=True)
    serializer_class = ReminderSerializer

    def perform_create(self, serializer):
        # Associate user if authenticated
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

    @action(detail=True, methods=['patch'])
    def snooze(self, request, pk=None):
        reminder = self.get_object()
        snooze_minutes = int(request.data.get('snooze_minutes', 15))
        
        reminder.snooze_until = timezone.now() + timedelta(minutes=snooze_minutes)
        # We don't change is_active, snoozed is just skipped until snooze_until passes
        reminder.save()
        
        return Response({'status': 'Reminder snoozed', 'snooze_until': reminder.snooze_until})

    @action(detail=True, methods=['patch'])
    def dismiss(self, request, pk=None):
        reminder = self.get_object()
        # Set is_active = False so it stops forever
        reminder.is_active = False
        reminder.save()
        return Response({'status': 'Reminder dismissed permanently'})

class FCMTokenRegisterView(APIView):
    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            user = request.user if request.user.is_authenticated else None
            
            # Create or update token
            fcm_token, created = FCMToken.objects.update_or_create(
                token=token,
                defaults={'user': user}
            )
            return Response({'status': 'Token registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
