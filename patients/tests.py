from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from patients.models import Patient


class PatientTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username="admin_test",
            email="admin@test.com",
            password="StrongPass123",
            role="admin",
        )

        self.patient_user = User.objects.create_user(
            username="patient_test",
            email="patient@test.com",
            password="StrongPass123",
            first_name="Test",
            last_name="Patient",
            role="patient",
        )

        self.second_patient_user = User.objects.create_user(
            username="patient_two",
            email="patient2@test.com",
            password="StrongPass123",
            first_name="John",
            last_name="Smith",
            role="patient",
        )

    def test_unauthenticated_user_cannot_access_patients(self):
        response = self.client.get("/api/patients/")

        self.assertEqual(response.status_code, 401)

    def test_admin_can_create_patient(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/patients/",
            {
                "user": self.patient_user.id,
                "date_of_birth": "2000-01-01",
                "gender": "Male",
                "blood_group": "O+",
                "address": "Lagos",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Patient.objects.filter(
                user=self.patient_user
            ).exists()
        )

    def test_patient_can_only_see_their_own_profile(self):
        Patient.objects.create(
            user=self.patient_user,
            date_of_birth="2000-01-01",
            gender="Male",
            blood_group="O+",
            address="Lagos",
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get("/api/patients/")

        self.assertEqual(response.status_code, 200)

        results = response.data["results"]

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["user"],
            self.patient_user.id
        )

    def test_admin_can_search_patients(self):
        Patient.objects.create(
            user=self.patient_user,
            date_of_birth="2000-01-01",
            gender="Male",
            blood_group="O+",
            address="Lagos",
        )

        Patient.objects.create(
            user=self.second_patient_user,
            date_of_birth="1999-01-01",
            gender="Female",
            blood_group="A+",
            address="Abuja",
        )

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            "/api/patients/?search=John"
        )

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["user"],
            self.second_patient_user.id,
        )

    def test_admin_can_create_patient_with_genotype(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/patients/",
            {
                "user": self.patient_user.id,
                "date_of_birth": "2000-01-01",
                "gender": "Male",
                "blood_group": "O+",
                "genotype": "AS",
                "address": "Lagos",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        patient = Patient.objects.get(
            user=self.patient_user
        )

        self.assertEqual(
            patient.genotype,
            "AS"
        )

