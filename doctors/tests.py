from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

from accounts.models import User
from departments.models import Department
from doctors.models import Doctor


class DoctorTests(TestCase):

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
            first_name="John",
            last_name="Doctor",
            role="doctor",
        )

        self.second_doctor_user = User.objects.create_user(
            username="doctor_two",
            email="doctor2@test.com",
            password="StrongPass123",
            first_name="Jane",
            last_name="Specialist",
            role="doctor",
        )

        self.patient_user = User.objects.create_user(
            username="patient_test",
            email="patient@test.com",
            password="StrongPass123",
            role="patient",
        )

        self.department = Department.objects.create(
            name="General Medicine",
            description="General medical care",
        )

        self.second_department = Department.objects.create(
            name="Cardiology",
            description="Heart and cardiovascular care",
        )

    def test_unauthenticated_user_cannot_access_doctors(self):
        response = self.client.get("/api/doctors/")
        self.assertEqual(response.status_code, 401)

    def test_admin_can_create_doctor(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/doctors/",
            {
                "user": self.doctor_user.id,
                "department": self.department.id,
                "specialization": "General Medicine",
                "license_number": "DOC-TEST-001",
                "years_of_experience": 5,
                "consultation_fee": "5000.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Doctor.objects.filter(
                user=self.doctor_user
            ).exists()
        )

    def test_non_admin_cannot_create_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)

        response = self.client.post(
            "/api/doctors/",
            {
                "user": self.doctor_user.id,
                "department": self.department.id,
                "specialization": "General Medicine",
                "license_number": "DOC-TEST-002",
                "years_of_experience": 5,
                "consultation_fee": "5000.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_can_search_doctors_by_specialization(self):
        Doctor.objects.create(
            user=self.doctor_user,
            department=self.department,
            specialization="General Medicine",
            license_number="DOC-SEARCH-001",
            years_of_experience=5,
            consultation_fee=5000,
        )

        Doctor.objects.create(
            user=self.second_doctor_user,
            department=self.second_department,
            specialization="Cardiology",
            license_number="DOC-SEARCH-002",
            years_of_experience=8,
            consultation_fee=8000,
        )

        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get(
            "/api/doctors/?search=Cardiology"
        )

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["specialization"],
            "Cardiology",
        )

    def test_can_filter_doctors_by_department(self):
        Doctor.objects.create(
            user=self.doctor_user,
            department=self.department,
            specialization="General Medicine",
            license_number="DOC-FILTER-001",
            years_of_experience=5,
            consultation_fee=5000,
        )

        Doctor.objects.create(
            user=self.second_doctor_user,
            department=self.second_department,
            specialization="Cardiology",
            license_number="DOC-FILTER-002",
            years_of_experience=8,
            consultation_fee=8000,
        )

        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get(
            f"/api/doctors/?department={self.second_department.id}"
        )

        self.assertEqual(response.status_code, 200)

        results = (
            response.data["results"]
            if isinstance(response.data, dict)
            else response.data
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["department"],
            self.second_department.id,
        )

    def test_admin_can_upload_doctor_profile_photo(self):
        self.client.force_authenticate(user=self.admin)

        # Create a real image in memory
        image = Image.new("RGB", (100, 100), color="white")

        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        uploaded_image = SimpleUploadedFile(
            "doctor.png",
            image_buffer.getvalue(),
            content_type="image/png",
        )

        response = self.client.post(
            "/api/doctors/",
            {
                "user": self.doctor_user.id,
                "department": self.department.id,
                "specialization": "General Medicine",
                "license_number": "DOC-UPLOAD-001",
                "years_of_experience": 5,
                "consultation_fee": "5000.00",
                "profile_photo": uploaded_image,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)

        doctor = Doctor.objects.get(
            user=self.doctor_user
        )

        self.assertTrue(doctor.profile_photo)

