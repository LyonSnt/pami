from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

from apps.accounts.roles import (
    CONTACT_MANAGER_GROUP,
    CONTACT_MANAGER_PERMISSIONS,
    CONTENT_EDITOR_GROUP,
    CONTENT_EDITOR_PERMISSIONS,
)


class Command(BaseCommand):
    help = "Crea o actualiza los grupos administrativos oficiales de Pámi."

    def handle(self, *args, **options):
        role_definitions = {
            CONTENT_EDITOR_GROUP: CONTENT_EDITOR_PERMISSIONS,
            CONTACT_MANAGER_GROUP: CONTACT_MANAGER_PERMISSIONS,
        }

        for group_name, permission_map in role_definitions.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            permissions = self._get_permissions(permission_map)
            group.permissions.set(permissions)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Rol actualizado: {group_name} ({len(permissions)} permisos)."
                )
            )

    def _get_permissions(self, permission_map):
        permissions = []
        missing_permissions = []

        for app_label, codenames in permission_map.items():
            found_permissions = Permission.objects.filter(
                content_type__app_label=app_label,
                codename__in=codenames,
            )
            found_by_codename = {
                permission.codename: permission
                for permission in found_permissions
            }

            permissions.extend(found_by_codename.values())
            missing_permissions.extend(
                f"{app_label}.{codename}"
                for codename in codenames
                if codename not in found_by_codename
            )

        if missing_permissions:
            raise CommandError(
                "No se encontraron los permisos: "
                + ", ".join(sorted(missing_permissions))
            )

        return permissions
