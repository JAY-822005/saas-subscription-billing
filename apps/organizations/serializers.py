from rest_framework import serializers
from django.utils.text import slugify
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
            "updated_at",
        ]

        read_only_fields = [
            "owner",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        """Validate organization name is not empty and has reasonable length"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Organization name cannot be empty")
        if len(value) > 255:
            raise serializers.ValidationError("Organization name cannot exceed 255 characters")
        return value.strip()

    def validate_contact_email(self, value):
        """Validate contact email format"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Contact email is required")
        return value.lower()

    def validate_slug(self, value):
        """Validate slug is unique and properly formatted"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Slug cannot be empty")
        
        # Check for duplicate slug (excluding current instance in update case)
        instance = self.instance
        queryset = Organization.objects.filter(slug=value)
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(f"Organization with slug '{value}' already exists")
        
        return value.lower()

    def create(self, validated_data):
        """Create organization with auto-generated slug if not provided"""
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)