from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from departments.models import Department
from doctors.models import Doctor
from patients.models import Patient
from reviews.models import Review


class ReviewTests(TestCase):

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
            role="patient",
        )

        self.other_patient_user = User.objects.create_user(
            username="patient_two",
            email="patient2@test.com",
            password="StrongPass123",
            role="patient",
        )

        self.doctor_user = User.objects.create_user(
            username="doctor_test",
            email="doctor@test.com",
            password="StrongPass123",
            role="doctor",
        )

        self.patient = Patient.objects.create(
            user=self.patient_user,
            date_of_birth="2000-01-01",
            gender="Female",
            blood_group="O+",
            address="Lagos",
        )

        self.other_patient = Patient.objects.create(
            user=self.other_patient_user,
            date_of_birth="1999-01-01",
            gender="Male",
            blood_group="A+",
            address="Lagos",
        )

        self.department = Department.objects.create(
            name="General Medicine",
            description="General medical care",
        )

        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            department=self.department,
            specialization="General Medicine",
            license_number="DOC-REVIEW-001",
            years_of_experience=5,
            consultation_fee=5000,
        )

        self.review = Review.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            rating=5,
            feedback="Excellent doctor.",
        )

        self.other_review = Review.objects.create(
            patient=self.other_patient,
            doctor=self.doctor,
            rating=4,
            feedback="Very good service.",
        )

    def test_unauthenticated_user_cannot_access_reviews(self):
        response = self.client.get("/api/reviews/")
        self.assertEqual(response.status_code, 401)

    def test_patient_can_only_see_their_own_reviews(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["patient"], self.patient.id)

    def test_patient_can_create_review(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.post(
            "/api/reviews/",
            {
                "doctor": self.doctor.id,
                "rating": 5,
                "feedback": "Great experience.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Review.objects.filter(
                patient=self.patient,
                doctor=self.doctor,
                rating=5,
                feedback="Great experience.",
            ).exists()
        )

    def test_non_patient_cannot_create_review(self):
        self.client.force_authenticate(user=self.doctor_user)

        response = self.client.post(
            "/api/reviews/",
            {
                "doctor": self.doctor.id,
                "rating": 5,
                "feedback": "Great doctor.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)