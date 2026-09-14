from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from departments.models import Department
from laboratory.models import (
    LaboratoryRequest,
    LaboratoryResult,
)


class LaboratoryTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username="admin_test",
            email="admin@test.com",
            password="StrongPass123",
            role="admin",
        )

        self.doctor_user = User.objects.create_user(
            username="doctor_test",
            email="doctor@test.com",
            password="StrongPass123",
            role="doctor",
        )

        self.patient_user = User.objects.create_user(
            username="patient_test",
            email="patient@test.com",
            password="StrongPass123",
            role="patient",
        )

        self.lab_user = User.objects.create_user(
            username="lab_test",
            email="lab@test.com",
            password="StrongPass123",
            role="lab_technician",
        )

        self.department = Department.objects.create(
            name="General Medicine",
            description="General medical care",
        )

        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            department=self.department,
            specialization="General Medicine",
            license_number="DOC-LAB-001",
            years_of_experience=5,
            consultation_fee=5000,
        )

        self.patient = Patient.objects.create(
            user=self.patient_user,
            date_of_birth="2000-01-01",
            gender="Female",
            blood_group="O+",
            address="Lagos",
        )

        self.laboratory_request = LaboratoryRequest.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            test_name="Blood Test",
            description="Full blood count",
        )

    def test_unauthenticated_user_cannot_access_lab_requests(self):
        response = self.client.get(
            "/api/laboratory/requests/"
        )

        self.assertEqual(response.status_code, 401)

    def test_doctor_can_create_lab_request(self):
        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            "/api/laboratory/requests/",
            {
                "patient": self.patient.id,
                "doctor": self.doctor.id,
                "test_name": "Malaria Test",
                "description": "Test for malaria",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            LaboratoryRequest.objects.filter(
                patient=self.patient,
                doctor=self.doctor,
                test_name="Malaria Test",
            ).exists()
        )

    def test_patient_cannot_create_lab_request(self):
        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            "/api/laboratory/requests/",
            {
                "patient": self.patient.id,
                "doctor": self.doctor.id,
                "test_name": "Blood Test",
                "description": "Test",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_lab_technician_can_create_result(self):
        self.client.force_authenticate(
            user=self.lab_user
        )

        response = self.client.post(
            "/api/laboratory/results/",
            {
                "laboratory_request": self.laboratory_request.id,
                "result": "Normal",
                "notes": "No abnormalities detected.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            LaboratoryResult.objects.filter(
                laboratory_request=self.laboratory_request
            ).exists()
        )

    def test_patient_cannot_create_lab_result(self):
        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            "/api/laboratory/results/",
            {
                "laboratory_request": self.laboratory_request.id,
                "result": "Normal",
                "notes": "Test result.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)