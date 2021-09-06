from django.test import TestCase
"""
This import allows for the provider pattern, where get_user_model
can be overidden to provide what ever user model is needed
"""
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):

    def test_should_create_user_with_email_successful(self):
        # Given
        email = "jimmy.jenkins@click.com"
        password = "Password1"

        # When
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # Then
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_should_create_new_user_with_email_normilised(self):
        # Given
        email = 'test@clickTRAVEL.com'

        # When
        user = get_user_model().objects.create_user(email, 'test123')

        # Then
        self.assertEquals(user.email, email.lower())

    def test_should_not_create_new_user_with_invalid_email(self):
        # Given/ Then
        with self.assertRaises(ValueError):
            # When
            get_user_model().objects.create_user(None, 'test123')

    def test_should_create_new_super_user(self):
        # Given / When
        user = get_user_model().objects.create_superuser(
            "james.b@matrix.com",
            "Password1"
        )

        # Then
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
