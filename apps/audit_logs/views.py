from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    
    # Add search and filtering
    search_fields = ['action', 'model_name', 'user__email']
    filterset_fields = ['action', 'model_name', 'organization']
    ordering_fields = ['created_at', 'action']
    ordering = ["-created_at"]

    def get_queryset(self):
        return AuditLog.objects.filter(
            organization__owner=self.request.user
        ).select_related('user', 'organization').order_by("-created_at")