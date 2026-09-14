from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

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
            return LaboratoryRequest.objects.filter(doctor__user=user)

        if user.role == "patient":
            return LaboratoryRequest.objects.filter(patient__user=user)

        if user.role == "lab_technician":
            return LaboratoryRequest.objects.all()

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
            return LaboratoryResult.objects.all()

        return LaboratoryResult.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role not in ["admin", "lab_technician"]:
            raise PermissionDenied(
                "Only administrators or laboratory technicians can create laboratory results."
            )

        serializer.save()

