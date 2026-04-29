from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PaymentRecovery
from .serializers import PaymentRecoverySerializer


class PaymentRecoveryViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentRecoverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentRecovery.objects.filter(
            organization__owner=self.request.user
        ).order_by("-created_at")