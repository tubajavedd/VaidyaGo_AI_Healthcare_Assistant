from rest_framework import generics, permissions
from .models import UpdateLog
from .serializers import UpdateLogSerializers


class createUpdateLogView(generics.CreateAPIView):
    serializer_class = UpdateLogSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateLogHistoryView(generics.ListAPIView):
    serializer_class = UpdateLogSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UpdateLog.objects.filter(
            user=self.request.user
        ).order_by("-created_at")
