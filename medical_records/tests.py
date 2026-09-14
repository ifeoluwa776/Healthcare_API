from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from departments.models import Department
from medical_records.models import MedicalRecord


class MedicalRecordTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.doctor_user = User.objects.create_user(
            username="doctor_test",
            email="doctor@test.com",
            password="StrongPass123",
            first_name="John",
            last_name="Doctor",
            role="doctor",
        )

        self.patient_user = User.objects.create_user(
            username="patient_test",
            email="patient@test.com",
            password="StrongPass123",
            first_name="Jane",
            last_name="Patient",
            role="patient",
        )

        self.other_patient_user = User.objects.create_user(
            username="patient_two",
            email="patient2@test.com",
            password="StrongPass123",
            role="patient",
        )

        self.admin = User.objects.create_user(
            username="admin_test",
            email="admin@test.com",
            password="StrongPass123",
            role="admin",
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

    def test_unauthenticated_user_cannot_access_medical_records(self):
        response = self.client.get(
            "/api/medical-records/"
        )

        self.assertEqual(response.status_code, 401)

    def test_doctor_can_create_medical_record(self):
        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            "/api/medical-records/",
            {
                "patient": self.patient.id,
                "doctor": self.doctor.id,
                "diagnosis": "Malaria",
                "symptoms": "Fever and headache",
                "treatment": "Medication and rest",
                "consultation_notes": "Patient advised to rest.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            MedicalRecord.objects.filter(
                patient=self.patient,
                doctor=self.doctor,
                diagnosis="Malaria",
            ).exists()
        )

    def test_patient_can_only_see_their_own_medical_records(self):
        MedicalRecord.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            diagnosis="Malaria",
            symptoms="Fever",
            treatment="Medication",
            consultation_notes="Rest advised.",
        )

        MedicalRecord.objects.create(
            patient=self.other_patient,
            doctor=self.doctor,
            diagnosis="Flu",
            symptoms="Cough",
            treatment="Medication",
            consultation_notes="Follow-up required.",
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            "/api/medical-records/"
        )

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["patient"],
            self.patient.id
        )

    def test_patient_cannot_create_medical_record(self):
        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            "/api/medical-records/",
            {
                "patient": self.patient.id,
                "doctor": self.doctor.id,
                "diagnosis": "Malaria",
                "symptoms": "Fever",
                "treatment": "Medication",
                "consultation_notes": "Test record.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_can_filter_medical_records_by_patient(self):
        first_record = MedicalRecord.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            diagnosis="Malaria",
            symptoms="Fever",
            treatment="Medication",
            consultation_notes="Rest advised.",
        )

        MedicalRecord.objects.create(
            patient=self.other_patient,
            doctor=self.doctor,
            diagnosis="Flu",
            symptoms="Cough",
            treatment="Medication",
            consultation_notes="Follow-up required.",
        )

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            f"/api/medical-records/?patient={self.patient.id}"
        )

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["id"],
            first_record.id,
        )

    def test_doctor_can_upload_medical_record_attachment(self):
        self.client.force_authenticate(
            user=self.doctor_user
        )

        attachment = SimpleUploadedFile(
            "medical_report.pdf",
            b"Sample medical report document",
            content_type="application/pdf",
        )

        response = self.client.post(
            "/api/medical-records/",
            {
                "patient": self.patient.id,
                "doctor": self.doctor.id,
                "diagnosis": "Malaria",
                "symptoms": "Fever and headache",
                "treatment": "Medication and rest",
                "consultation_notes": "Patient advised to rest.",
                "attachments": attachment,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)

        record = MedicalRecord.objects.get(
            patient=self.patient,
            diagnosis="Malaria",
        )

        self.assertTrue(record.attachments)
