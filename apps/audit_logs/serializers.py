from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_email = serializers.ReadOnlyField(
        source="actor.email"
    )

    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    class Meta:
        model = AuditLog
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
        ]