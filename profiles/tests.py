from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileTest(TestCase):
    """
    A function to test profile creation.
    """
    def setUp(self):
        """
        Creates a test user.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_profile_creation(self):
        """
        A function to test profile creation.
        """
        self.assertIsInstance(self.user.profile, Profile)
