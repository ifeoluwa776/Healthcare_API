from django.test import TestCase
from rest_framework.test import APIClient

from .models import User


class AccountTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        response = self.client.post(
            "/api/accounts/register/",
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "StrongPass123",
                "first_name": "Test",
                "last_name": "User",
                "role": "patient",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            User.objects.filter(username="testuser").exists()
        )

    def test_user_login(self):
        User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="StrongPass123",
            role="patient",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "username": "loginuser",
                "password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_requires_authentication(self):
        response = self.client.get(
            "/api/accounts/profile/"
        )

        self.assertEqual(response.status_code, 401)