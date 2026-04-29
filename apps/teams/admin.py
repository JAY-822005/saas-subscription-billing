from django.contrib import admin
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "organization",
        "role",
        "is_active",
        "joined_at",
    )

    search_fields = (
        "user__email",
        "organization__name",
    )

    list_filter = (
        "role",
        "is_active",
    )