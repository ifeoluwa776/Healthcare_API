from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from departments.models import Department


class DepartmentTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username="admin_test",
            email="admin@test.com",
            password="StrongPass123",
            role="admin",
        )

        self.doctor = User.objects.create_user(
            username="doctor_test",
            email="doctor@test.com",
            password="StrongPass123",
            role="doctor",
        )

    def test_unauthenticated_user_cannot_access_departments(self):
        response = self.client.get("/api/departments/")

        self.assertEqual(response.status_code, 401)

    def test_admin_can_create_department(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/departments/",
            {
                "name": "General Medicine",
                "description": "General medical care",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Department.objects.filter(
                name="General Medicine"
            ).exists()
        )

    def test_department_name_must_be_unique(self):
        Department.objects.create(
            name="General Medicine",
            description="General medical care",
        )

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/departments/",
            {
                "name": "General Medicine",
                "description": "Another description",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)