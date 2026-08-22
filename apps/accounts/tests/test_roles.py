from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.accounts.roles import (
    CONTACT_MANAGER_GROUP,
    CONTACT_MANAGER_PERMISSIONS,
    CONTENT_EDITOR_GROUP,
    CONTENT_EDITOR_PERMISSIONS,
)


class SetupAdminRolesCommandTests(TestCase):
    def test_command_creates_official_roles_with_exact_permissions(self):
        call_command("setup_admin_roles", verbosity=0)

        self.assert_role_permissions(
            CONTENT_EDITOR_GROUP,
            CONTENT_EDITOR_PERMISSIONS,
        )
        self.assert_role_permissions(
            CONTACT_MANAGER_GROUP,
            CONTACT_MANAGER_PERMISSIONS,
        )

    def test_command_is_idempotent_and_removes_unofficial_permissions(self):
        call_command("setup_admin_roles", verbosity=0)
        editor_group = Group.objects.get(name=CONTENT_EDITOR_GROUP)
        extra_permission = Permission.objects.get(
            content_type__app_label="accounts",
            codename="change_user",
        )
        editor_group.permissions.add(extra_permission)

        call_command("setup_admin_roles", verbosity=0)

        self.assertEqual(
            Group.objects.filter(name=CONTENT_EDITOR_GROUP).count(),
            1,
        )
        self.assertEqual(
            Group.objects.filter(name=CONTACT_MANAGER_GROUP).count(),
            1,
        )
        self.assertTrue(editor_group.permissions.exists())
        self.assertFalse(editor_group.permissions.filter(pk=extra_permission.pk).exists())

    def assert_role_permissions(self, group_name, permission_map):
        group = Group.objects.get(name=group_name)
        actual_permissions = {
            (permission.content_type.app_label, permission.codename)
            for permission in group.permissions.select_related("content_type")
        }
        expected_permissions = {
            (app_label, codename)
            for app_label, codenames in permission_map.items()
            for codename in codenames
        }

        self.assertEqual(actual_permissions, expected_permissions)


class AdministrativeRoleAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("setup_admin_roles", verbosity=0)

    def test_content_editor_access_is_limited_to_editorial_modules(self):
        editor = self.create_staff_user("editor", CONTENT_EDITOR_GROUP)
        self.client.force_login(editor)

        self.assertEqual(
            self.client.get(reverse("admin:catalog_product_changelist")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("admin:catalog_productfeature_changelist")
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("admin:catalog_productimage_changelist")
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("admin:accounts_user_changelist")).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(reverse("admin:audit_auditlog_changelist")).status_code,
            403,
        )

    def test_contact_manager_access_is_limited_to_messages(self):
        manager = self.create_staff_user("contact-manager", CONTACT_MANAGER_GROUP)
        self.client.force_login(manager)

        self.assertEqual(
            self.client.get(reverse("admin:contact_contactmessage_changelist")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("admin:catalog_product_changelist")).status_code,
            403,
        )

    @staticmethod
    def create_staff_user(username, group_name):
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password="test-password",
            is_staff=True,
        )
        user.groups.add(Group.objects.get(name=group_name))
        return user
