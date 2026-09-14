from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Prescription
from .serializers import PrescriptionSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related(
        "medical_record",
        "medical_record__doctor",
        "medical_record__patient",
    ).all()

    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "medical_record",
    ]

    search_fields = [
        "medication_name",
        "dosage",
        "instructions",
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return self.queryset

        if user.role == "doctor":
            return self.queryset.filter(
                medical_record__doctor__user=user
            )

        if user.role == "patient":
            return self.queryset.filter(
                medical_record__patient__user=user
            )

        return self.queryset.none()

    def perform_create(self, serializer):
        if self.request.user.role != "doctor":
            raise PermissionDenied(
                "Only doctors can create prescriptions."
            )

        serializer.save()

    @action(
        detail=True,
        methods=["get"],
        url_path="download",
    )
    def download(self, request, pk=None):
        prescription = self.get_object()

        doctor = prescription.medical_record.doctor
        patient = prescription.medical_record.patient

        content = f"""
HEALTHCARE MANAGEMENT SYSTEM
PRESCRIPTION
==============================

Prescription ID: {prescription.id}

Patient:
{patient.user.first_name} {patient.user.last_name}

Doctor:
Dr. {doctor.user.first_name} {doctor.user.last_name}

Medication:
{prescription.medication_name}

Dosage:
{prescription.dosage}

Instructions:
{prescription.instructions}

Date:
{prescription.created_at}

==============================
"""

        response = HttpResponse(
            content.strip(),
            content_type="text/plain",
        )

        response["Content-Disposition"] = (
            f'attachment; filename="prescription_{prescription.id}.txt"'
        )

        return response

