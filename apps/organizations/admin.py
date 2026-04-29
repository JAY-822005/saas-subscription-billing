from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "owner",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
        "owner__email",
    )

    list_filter = (
        "is_active",
        "created_at",
    )