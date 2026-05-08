from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

from .models import SubscriptionPlan, Subscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    price_display = serializers.SerializerMethodField()
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "description",
            "monthly_price",
            "yearly_price",
            "price_display",
            "max_users",
            "usage_limit",
            "free_trial_days",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "price_display",
        ]

    def get_price_display(self, obj):
        """Return formatted price display"""
        return f"${obj.monthly_price}/month or ${obj.yearly_price}/year"

    def validate_monthly_price(self, value):
        """Validate monthly price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Monthly price must be greater than 0")
        return value

    def validate_yearly_price(self, value):
        """Validate yearly price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Yearly price must be greater than 0")
        return value

    def validate_max_users(self, value):
        """Validate max users is positive"""
        if value < 1:
            raise serializers.ValidationError("Maximum users must be at least 1")
        return value

    def validate_free_trial_days(self, value):
        """Validate trial days are non-negative"""
        if value < 0:
            raise serializers.ValidationError("Free trial days cannot be negative")
        return value


class SubscriptionSerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    plan_name = serializers.ReadOnlyField(
        source="plan.name"
    )

    plan_details = SubscriptionPlanSerializer(
        source="plan",
        read_only=True
    )

    class Meta:
        model = Subscription
        fields = [
            "id",
            "organization",
            "organization_name",
            "plan",
            "plan_name",
            "plan_details",
            "status",
            "billing_cycle",
            "trial_ends_at",
            "starts_at",
            "renews_at",
            "cancelled_at",
            "auto_renew",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "starts_at",
            "organization_name",
            "plan_name",
            "plan_details",
        ]

    def validate_organization(self, value):
        """Validate organization is active"""
        if not value.is_active:
            raise serializers.ValidationError("Cannot create subscription for inactive organization")
        return value

    def validate_plan(self, value):
        """Validate plan is active"""
        if not value.is_active:
            raise serializers.ValidationError("Cannot subscribe to inactive plan")
        return value

    def validate(self, data):
        """Validate subscription status transitions"""
        # Check if organization already has a subscription
        if self.instance is None:  # Only check on create
            organization = data.get("organization")
            if Subscription.objects.filter(organization=organization).exists():
                raise serializers.ValidationError(
                    "Organization already has an active subscription"
                )
        return data

    def create(self, validated_data):
        """Create subscription with proper date calculations"""
        plan = validated_data["plan"]
        billing_cycle = validated_data["billing_cycle"]

        # Calculate trial end date
        trial_end = timezone.now() + timedelta(days=plan.free_trial_days)

        # Calculate renewal date based on billing cycle
        if billing_cycle == "monthly":
            renew_date = timezone.now() + timedelta(days=30)
        else:  # yearly
            renew_date = timezone.now() + timedelta(days=365)

        validated_data["trial_ends_at"] = trial_end
        validated_data["renews_at"] = renew_date
        validated_data["status"] = "trial"

        return super().create(validated_data)