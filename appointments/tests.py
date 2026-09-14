from django.test import TestCase, override_settings
from django.core import mail
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from departments.models import Department
from appointments.models import Appointment


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
)
class AppointmentTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.patient_user = User.objects.create_user(
            username="patient1",
            email="patient@example.com",
            password="StrongPass123",
            role="patient",
        )

        self.doctor_user = User.objects.create_user(
            username="doctor1",
            email="doctor@example.com",
            password="StrongPass123",
            role="doctor",
        )

        self.patient = Patient.objects.create(
            user=self.patient_user,
            date_of_birth="2000-01-01",
            gender="Male",
            blood_group="O+",
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
            license_number="DOC-TEST-001",
            years_of_experience=5,
            consultation_fee=5000,
        )

    def test_unauthenticated_user_cannot_access_appointments(self):
        response = self.client.get(
            "/api/appointments/"
        )

        self.assertEqual(response.status_code, 401)

    def test_patient_can_create_appointment(self):
        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            "/api/appointments/",
            {
                "patient": self.patient.id,
                "doctor": self.doctor.id,
                "appointment_date": (
                    timezone.now() + timedelta(days=2)
                ).isoformat(),
                "reason": "General check-up",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Appointment.objects.count(),
            1
        )

    def test_appointment_cannot_be_booked_in_the_past(self):
        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            "/api/appointments/",
            {
                "patient": self.patient.id,
                "doctor": self.doctor.id,
                "appointment_date": (
                    timezone.now() - timedelta(days=1)
                ).isoformat(),
                "reason": "Check-up",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_patient_can_view_their_appointments(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=(
                timezone.now() + timedelta(days=2)
            ),
            reason="Routine check-up",
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            "/api/appointments/"
        )

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0]["id"],
            appointment.id,
        )

    def test_patient_can_receive_appointment_reminder(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=(
                timezone.now() + timedelta(days=2)
            ),
            reason="Routine check-up",
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            f"/api/appointments/{appointment.id}/remind/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(mail.outbox),
            1
        )

        email = mail.outbox[0]

        self.assertEqual(
            email.to,
            ["patient@example.com"]
        )

        self.assertEqual(
            email.subject,
            "Appointment Reminder"
        )

        self.assertIn(
            "appointment",
            email.body.lower()
        )

