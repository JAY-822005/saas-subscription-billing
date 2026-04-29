from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(
        source="owner.email"
    )

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "owner",
            "owner_email",
            "contact_email",
            "is_active",
            "trial_ends_at",
            "created_at",
        ]

        read_only_fields = [
            "owner",
            "created_at",
        ]