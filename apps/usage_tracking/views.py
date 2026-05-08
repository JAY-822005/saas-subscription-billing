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
    
    # Add search and filtering
    search_fields = ['feature_name', 'organization__name']
    filterset_fields = ['feature_name', 'organization', 'is_over_limit']
    ordering_fields = ['created_at', 'billing_month']
    ordering = ["-created_at"]

    def get_queryset(self):
        return UsageRecord.objects.filter(
            organization__owner=self.request.user
        ).select_related('organization', 'subscription_plan').order_by("-created_at")

    @action(detail=True, methods=["get"])
    def recommendation(self, request, pk=None):
        usage = self.get_object()
        data = check_upgrade_recommendation(usage)
        return Response(data)