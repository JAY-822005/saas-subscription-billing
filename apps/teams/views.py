from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import TeamMember
from .serializers import TeamMemberSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]
    
    # Add search and filtering
    search_fields = ['user__email', 'user__username']
    filterset_fields = ['role', 'organization']
    ordering_fields = ['joined_at', 'user__email']
    ordering = ["-joined_at"]

    def get_queryset(self):
        return TeamMember.objects.filter(
            organization__owner=self.request.user
        ).select_related('user', 'organization').order_by("-joined_at")