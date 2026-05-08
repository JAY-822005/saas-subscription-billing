from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import SubscriptionPlan, Subscription
from .serializers import (
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
)


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Subscription Plans.
    
    Only authenticated users can view available plans.
    Plans are shared across all organizations.
    """
    queryset = SubscriptionPlan.objects.filter(
        is_active=True
    ).order_by("monthly_price")

    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["monthly_price", "yearly_price", "created_at"]


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Subscriptions.
    
    Users can only view/edit their own organization's subscriptions.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "billing_cycle"]
    search_fields = ["organization__name", "plan__name"]
    ordering_fields = ["created_at", "renews_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return subscriptions for user's organizations only"""
        return Subscription.objects.filter(
            organization__owner=self.request.user
        ).select_related(
            "organization",
            "plan"
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

    def perform_update(self, serializer):
        """Prevent critical field changes"""
        # Prevent organization change
        if "organization" in serializer.validated_data:
            serializer.validated_data.pop("organization")
        
        # Prevent plan change
        if "plan" in serializer.validated_data:
            serializer.validated_data.pop("plan")
        
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Delete not allowed - subscriptions should be cancelled instead"""
        return Response(
            {"detail": "Use cancellation endpoint instead of delete"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )