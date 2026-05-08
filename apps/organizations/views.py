from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    
    # Add search and filtering
    search_fields = ['name', 'email']
    filterset_fields = ['is_active']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Organization.objects.filter(
            owner=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)