from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Invoices.
    
    Users can only view/edit their own organization's invoices.
    """
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "organization"]
    search_fields = ["invoice_number", "organization__name"]
    ordering_fields = ["created_at", "due_date", "amount"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return invoices for user's organizations only"""
        return Invoice.objects.filter(
            organization__owner=self.request.user
        ).select_related(
            "organization",
            "subscription"
        ).order_by("-created_at")

    def perform_create(self, serializer):
        """Validate organization ownership on create"""
        organization = serializer.validated_data.get("organization")
        
        # Verify user owns the organization
        if organization.owner != self.request.user:
            return Response(
                {"detail": "You do not own this organization"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save()

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        """Mark invoice as paid"""
        invoice = self.get_object()
        
        if invoice.status == "paid":
            return Response(
                {"detail": "Invoice is already marked as paid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invoice.status = "paid"
        invoice.paid_at = timezone.now()
        invoice.save()
        
        return Response(
            InvoiceSerializer(invoice).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def mark_overdue(self, request, pk=None):
        """Mark invoice as overdue"""
        invoice = self.get_object()
        
        if invoice.status == "paid":
            return Response(
                {"detail": "Cannot mark paid invoice as overdue"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invoice.status = "overdue"
        invoice.save()
        
        return Response(
            InvoiceSerializer(invoice).data,
            status=status.HTTP_200_OK
        )