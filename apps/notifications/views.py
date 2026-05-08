from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    # Add search and filtering
    search_fields = ['title', 'message', 'organization__name']
    filterset_fields = ['is_read', 'notification_type', 'organization']
    ordering_fields = ['created_at', 'is_read']
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notification.objects.filter(
            organization__owner=self.request.user
        ).select_related('organization').order_by("-created_at")