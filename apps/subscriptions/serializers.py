from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

from .models import SubscriptionPlan, Subscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    plan_name = serializers.ReadOnlyField(
        source="plan.name"
    )

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "starts_at",
            "trial_ends_at",
            "renews_at",
            "cancelled_at",
        ]

    def create(self, validated_data):
        plan = validated_data["plan"]

        trial_end = timezone.now() + timedelta(
            days=plan.free_trial_days
        )

        renew_date = timezone.now() + timedelta(days=30)

        validated_data["trial_ends_at"] = trial_end
        validated_data["renews_at"] = renew_date
        validated_data["status"] = "trial"

        return super().create(validated_data)