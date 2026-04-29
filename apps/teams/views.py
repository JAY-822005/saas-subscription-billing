from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import TeamMember
from .serializers import TeamMemberSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamMember.objects.filter(
            organization__owner=self.request.user
        ).order_by("-joined_at")