from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from departments.models import Department
from medical_records.models import MedicalRecord
from prescriptions.models import Prescription


class PrescriptionTests(TestCase):

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

        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            diagnosis="Malaria",
            symptoms="Fever and headache",
            treatment="Medication and rest",
            consultation_notes="Rest advised.",
        )

        self.other_medical_record = MedicalRecord.objects.create(
            patient=self.other_patient,
            doctor=self.doctor,
            diagnosis="Flu",
            symptoms="Cough",
            treatment="Medication",
            consultation_notes="Follow-up required.",
        )

    def test_unauthenticated_user_cannot_access_prescriptions(self):
        response = self.client.get(
            "/api/prescriptions/"
        )

        self.assertEqual(response.status_code, 401)

    def test_doctor_can_create_prescription(self):
        self.client.force_authenticate(
            user=self.doctor_user
        )

        response = self.client.post(
            "/api/prescriptions/",
            {
                "medical_record": self.medical_record.id,
                "medication_name": "Paracetamol",
                "dosage": "500mg",
                "instructions": "Take twice daily.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Prescription.objects.filter(
                medical_record=self.medical_record,
                medication_name="Paracetamol",
            ).exists()
        )

    def test_patient_can_only_see_their_own_prescriptions(self):
        Prescription.objects.create(
            medical_record=self.medical_record,
            medication_name="Paracetamol",
            dosage="500mg",
            instructions="Take twice daily.",
        )

        Prescription.objects.create(
            medical_record=self.other_medical_record,
            medication_name="Ibuprofen",
            dosage="400mg",
            instructions="Take once daily.",
        )

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            "/api/prescriptions/"
        )

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["medical_record"],
            self.medical_record.id
        )

    def test_patient_cannot_create_prescription(self):
        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.post(
            "/api/prescriptions/",
            {
                "medical_record": self.medical_record.id,
                "medication_name": "Paracetamol",
                "dosage": "500mg",
                "instructions": "Take twice daily.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)