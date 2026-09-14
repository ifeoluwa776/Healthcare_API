from django.http import FileResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from .models import LaboratoryRequest, LaboratoryResult
from .serializers import (
    LaboratoryRequestSerializer,
    LaboratoryResultSerializer,
)


class LaboratoryRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LaboratoryRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return LaboratoryRequest.objects.all()

        if user.role == "doctor":
            return LaboratoryRequest.objects.filter(
                doctor__user=user
            )

        if user.role == "patient":
            return LaboratoryRequest.objects.filter(
                patient__user=user
            )

        if user.role == "lab_technician":
            return LaboratoryRequest.objects.filter(
                laboratory_technician=user
            )

        return LaboratoryRequest.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role not in ["admin", "doctor"]:
            raise PermissionDenied(
                "Only administrators or doctors can create laboratory requests."
            )

        serializer.save()


class LaboratoryResultViewSet(viewsets.ModelViewSet):
    serializer_class = LaboratoryResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return LaboratoryResult.objects.all()

        if user.role == "doctor":
            return LaboratoryResult.objects.filter(
                laboratory_request__doctor__user=user
            )

        if user.role == "patient":
            return LaboratoryResult.objects.filter(
                laboratory_request__patient__user=user
            )

        if user.role == "lab_technician":
            return LaboratoryResult.objects.filter(
                laboratory_request__laboratory_technician=user
            )

        return LaboratoryResult.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role not in ["admin", "lab_technician"]:
            raise PermissionDenied(
                "Only administrators or laboratory technicians can create laboratory results."
            )

        laboratory_request = serializer.validated_data[
            "laboratory_request"
        ]

        if self.request.user.role == "lab_technician":
            if laboratory_request.laboratory_technician != self.request.user:
                raise PermissionDenied(
                    "You are not assigned to this laboratory request."
                )

        serializer.save()

    @action(
        detail=True,
        methods=["get"],
        url_path="download",
    )
    def download(self, request, pk=None):
        laboratory_result = self.get_object()

        if not laboratory_result.report:
            return PermissionDenied(
                "No laboratory report is available for download."
            )

        response = FileResponse(
            laboratory_result.report.open("rb"),
            as_attachment=True,
            filename=laboratory_result.report.name.split("/")[-1],
        )

        return response

