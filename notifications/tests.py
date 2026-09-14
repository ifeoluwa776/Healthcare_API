from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from notifications.models import Notification


class NotificationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="user_test",
            email="user@test.com",
            password="StrongPass123",
            role="patient",
        )

        self.other_user = User.objects.create_user(
            username="other_user",
            email="other@test.com",
            password="StrongPass123",
            role="doctor",
        )

        self.notification = Notification.objects.create(
            user=self.user,
            title="Appointment Reminder",
            message="You have an appointment tomorrow.",
            notification_type="appointment",
        )

        self.other_notification = Notification.objects.create(
            user=self.other_user,
            title="Private Notification",
            message="This belongs to another user.",
            notification_type="general",
        )

    def test_unauthenticated_user_cannot_access_notifications(self):
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, 401)

    def test_user_can_see_only_their_notifications(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/notifications/")

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["user"], self.user.id)

    def test_user_can_create_notification(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/notifications/",
            {
                "title": "Test Notification",
                "message": "This is a test notification.",
                "notification_type": "general",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Notification.objects.filter(
                user=self.user,
                title="Test Notification",
            ).exists()
        )

    def test_user_cannot_create_notification_for_another_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/notifications/",
            {
                "user": self.other_user.id,
                "title": "Attempted Notification",
                "message": "This should not belong to another user.",
                "notification_type": "general",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        notification = Notification.objects.get(
            title="Attempted Notification"
        )

        self.assertEqual(notification.user, self.user)