from rest_framework import serializers

from .models import UsageRecord


class UsageRecordSerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    class Meta:
        model = UsageRecord
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_over_limit",
        ]