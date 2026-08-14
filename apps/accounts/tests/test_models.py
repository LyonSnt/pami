from django.test import TestCase

from apps.accounts.models import User


class UserProfileTests(TestCase):
    def test_profile_is_created_with_user(self):
        user = User.objects.create_user(
            username="profile-user",
            email="profile@example.com",
            password="test-password",
        )

        self.assertTrue(hasattr(user, "profile"))
        self.assertEqual(str(user.profile), f"Perfil de {user}")
