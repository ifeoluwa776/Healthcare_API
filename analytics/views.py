from django.db.models import Sum
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Invoice
from laboratory.models import LaboratoryRequest
from departments.models import Department


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "admin":
            today = timezone.localdate()

            daily_visits = Appointment.objects.filter(
                appointment_date__date=today
            ).count()

            revenue = Invoice.objects.filter(
                status="paid"
            ).aggregate(
                total=Sum("total_amount")
            )["total"] or 0

            department_performance = []

            for department in Department.objects.all():
                department_performance.append({
                    "department": department.name,
                    "doctors": department.doctors.count(),
                    "appointments": Appointment.objects.filter(
                        doctor__department=department
                    ).count(),
                    "completed_appointments": Appointment.objects.filter(
                        doctor__department=department,
                        status="Completed"
                    ).count(),
                })

            return Response({
                "total_patients": Patient.objects.count(),
                "total_doctors": Doctor.objects.count(),
                "total_appointments": Appointment.objects.count(),
                "daily_visits": daily_visits,
                "revenue": revenue,
                "total_lab_requests": LaboratoryRequest.objects.count(),
                "department_performance": department_performance,
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

            total_consultations = Appointment.objects.filter(
                doctor=doctor
            ).count()

            completed_appointments = Appointment.objects.filter(
                doctor=doctor,
                status="Completed"
            ).count()

            completion_rate = 0

            if total_consultations > 0:
                completion_rate = round(
                    (completed_appointments / total_consultations) * 100,
                    2
                )

            total_patients = Appointment.objects.filter(
                doctor=doctor
            ).values("patient").distinct().count()

            return Response({
                "doctor": str(doctor),
                "total_consultations": total_consultations,
                "total_patients": total_patients,
                "total_prescriptions": Prescription.objects.filter(
                    medical_record__doctor=doctor
                ).count(),
                "completed_appointments": completed_appointments,
                "appointment_completion_rate": completion_rate,
            })

        raise PermissionDenied(
            "Only administrators and doctors can access analytics."
        )