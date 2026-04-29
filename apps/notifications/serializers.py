from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "sent_at",
        ]