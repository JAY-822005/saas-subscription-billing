from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UsageRecord
from .serializers import UsageRecordSerializer
from .services import check_upgrade_recommendation


class UsageRecordViewSet(viewsets.ModelViewSet):
    serializer_class = UsageRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UsageRecord.objects.filter(
            organization__owner=self.request.user
        ).order_by("-created_at")

    @action(detail=True, methods=["get"])
    def recommendation(self, request, pk=None):
        usage = self.get_object()
        data = check_upgrade_recommendation(usage)
        return Response(data)