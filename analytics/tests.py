from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from departments.models import Department
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from prescriptions.models import Prescription
from billing.models import Invoice
from laboratory.models import LaboratoryRequest


class AnalyticsTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username="analytics_admin",
            email="analyticsadmin@test.com",
            password="StrongPass123",
            role="admin",
        )

        self.doctor_user = User.objects.create_user(
            username="analytics_doctor",
            email="analyticsdoctor@test.com",
            password="StrongPass123",
            role="doctor",
        )

        self.patient_user = User.objects.create_user(
            username="analytics_patient",
            email="analyticspatient@test.com",
            password="StrongPass123",
            role="patient",
        )

        self.department = Department.objects.create(
            name="Analytics Department",
            description="Test department",
        )

        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            department=self.department,
            specialization="General Medicine",
            license_number="ANALYTICS-LIC-001",
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

    def test_admin_can_access_analytics(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/analytics/")

        self.assertEqual(response.status_code, 200)

        self.assertIn("total_patients", response.data)
        self.assertIn("total_doctors", response.data)
        self.assertIn("total_appointments", response.data)
        self.assertIn("daily_visits", response.data)
        self.assertIn("revenue", response.data)
        self.assertIn("total_lab_requests", response.data)
        self.assertIn("department_performance", response.data)

    def test_doctor_can_access_analytics(self):
        self.client.force_authenticate(user=self.doctor_user)

        response = self.client.get("/api/analytics/")

        self.assertEqual(response.status_code, 200)

        self.assertIn("total_consultations", response.data)
        self.assertIn("total_patients", response.data)
        self.assertIn("total_prescriptions", response.data)
        self.assertIn(
            "appointment_completion_rate",
            response.data,
        )

    def test_patient_cannot_access_analytics(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get("/api/analytics/")

        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_cannot_access_analytics(self):
        response = self.client.get("/api/analytics/")

        self.assertEqual(response.status_code, 401)