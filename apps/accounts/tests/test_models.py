from django.test import TestCase

from apps.accounts.models import User, UserProfile


class UserProfileTests(TestCase):
    def test_profile_is_created_with_user(self):
        user = User.objects.create_user(
            username="profile-user",
            email="profile@example.com",
            password="test-password",
        )

        self.assertTrue(hasattr(user, "profile"))
        self.assertEqual(str(user.profile), f"Perfil de {user}")

    def test_profile_has_an_unambiguous_admin_label(self):
        self.assertEqual(UserProfile._meta.verbose_name, "Perfil de usuario")
        self.assertEqual(
            UserProfile._meta.verbose_name_plural,
            "Perfiles de usuario",
        )
