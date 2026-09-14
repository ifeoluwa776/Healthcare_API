from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from prescriptions.models import Prescription
from billing.models import Invoice


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "admin":
            return Response({
                "total_users": User.objects.count(),
                "total_patients": Patient.objects.count(),
                "total_doctors": Doctor.objects.count(),
                "total_appointments": Appointment.objects.count(),
                "total_medical_records": MedicalRecord.objects.count(),
                "total_prescriptions": Prescription.objects.count(),
                "total_invoices": Invoice.objects.count(),
                "appointment_status": {
                    "pending": Appointment.objects.filter(
                        status="Pending"
                    ).count(),
                    "approved": Appointment.objects.filter(
                        status="Approved"
                    ).count(),
                    "completed": Appointment.objects.filter(
                        status="Completed"
                    ).count(),
                    "cancelled": Appointment.objects.filter(
                        status="Cancelled"
                    ).count(),
                    "missed": Appointment.objects.filter(
                        status="Missed"
                    ).count(),
                },
            })

        if request.user.role == "doctor":
            doctor = request.user.doctor_profile

            return Response({
                "doctor": str(doctor),
                "total_appointments": Appointment.objects.filter(
                    doctor=doctor
                ).count(),
                "completed_appointments": Appointment.objects.filter(
                    doctor=doctor,
                    status="Completed"
                ).count(),
                "pending_appointments": Appointment.objects.filter(
                    doctor=doctor,
                    status="Pending"
                ).count(),
                "total_medical_records": MedicalRecord.objects.filter(
                    doctor=doctor
                ).count(),
                "total_prescriptions": Prescription.objects.filter(
                    medical_record__doctor=doctor
                ).count(),
                "total_laboratory_requests": doctor.laboratory_requests.count(),
            })

        raise PermissionDenied(
            "Only administrators and doctors can access analytics."
        )