from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User, UserProfile
from apps.audit.admin_mixins import AuditModelAdminMixin


@admin.register(User)
class CustomUserAdmin(AuditModelAdminMixin, UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )


@admin.register(UserProfile)
class UserProfileAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "timezone",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )
