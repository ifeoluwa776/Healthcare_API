from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from patients.models import Patient
from billing.models import Invoice, Payment


class BillingTests(TestCase):

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

        self.invoice = Invoice.objects.create(
            patient=self.patient,
            consultation_fee=5000,
            laboratory_charges=2000,
            medication_charges=1000,
        )

        self.other_invoice = Invoice.objects.create(
            patient=self.other_patient,
            consultation_fee=3000,
            laboratory_charges=1000,
            medication_charges=500,
        )

        self.payment = Payment.objects.create(
            invoice=self.invoice,
            patient=self.patient,
            amount=5000,
            payment_method="cash",
            status="paid",
        )

    def test_unauthenticated_user_cannot_access_invoices(self):
        response = self.client.get(
            "/api/billing/invoices/"
        )
        self.assertEqual(response.status_code, 401)

    def test_admin_can_create_invoice(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/billing/invoices/",
            {
                "patient": self.patient.id,
                "consultation_fee": 5000,
                "laboratory_charges": 2000,
                "medication_charges": 1000,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        invoice = Invoice.objects.order_by("-id").first()

        self.assertEqual(invoice.total_amount, 8000)

    def test_patient_cannot_create_invoice(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.post(
            "/api/billing/invoices/",
            {
                "patient": self.patient.id,
                "consultation_fee": 5000,
                "laboratory_charges": 2000,
                "medication_charges": 1000,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_patient_can_only_see_their_own_invoices(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get(
            "/api/billing/invoices/"
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

    def test_patient_can_make_payment_for_own_invoice(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.post(
            "/api/billing/payments/",
            {
                "invoice": self.invoice.id,
                "amount": 5000,
                "payment_method": "cash",
                "status": "paid",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Payment.objects.filter(
                invoice=self.invoice,
                patient=self.patient,
                amount=5000,
            ).exists()
        )

    def test_patient_cannot_pay_other_patients_invoice(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.post(
            "/api/billing/payments/",
            {
                "invoice": self.other_invoice.id,
                "amount": 3000,
                "payment_method": "cash",
                "status": "paid",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_patient_can_generate_own_payment_receipt(self):
        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get(
            f"/api/billing/payments/{self.payment.id}/receipt/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "text/plain"
        )
        self.assertIn(
            "PAYMENT RECEIPT",
            response.content.decode()
        )
        self.assertIn(
            "5000.00",
            response.content.decode()
        )

    def test_patient_cannot_generate_other_patient_receipt(self):
        other_payment = Payment.objects.create(
            invoice=self.other_invoice,
            patient=self.other_patient,
            amount=3000,
            payment_method="cash",
            status="paid",
        )

        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get(
            f"/api/billing/payments/{other_payment.id}/receipt/"
        )

        self.assertEqual(response.status_code, 403)