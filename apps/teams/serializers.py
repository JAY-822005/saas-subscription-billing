from rest_framework import serializers
from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(
        source="user.email"
    )

    organization_name = serializers.ReadOnlyField(
        source="organization.name"
    )

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "user",
            "user_email",
            "organization",
            "organization_name",
            "role",
            "is_active",
            "joined_at",
        ]

        read_only_fields = [
            "joined_at",
        ]