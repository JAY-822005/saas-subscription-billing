from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PaymentRecovery
from .serializers import PaymentRecoverySerializer


class PaymentRecoveryViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentRecoverySerializer
    permission_classes = [IsAuthenticated]
    
    # Add search and filtering
    search_fields = ['invoice__invoice_number', 'organization__name']
    filterset_fields = ['status', 'organization']
    ordering_fields = ['created_at', 'next_retry_at']
    ordering = ["-created_at"]

    def get_queryset(self):
        return PaymentRecovery.objects.filter(
            organization__owner=self.request.user
        ).select_related('invoice', 'organization').order_by("-created_at")