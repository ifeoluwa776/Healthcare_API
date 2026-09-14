from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    search_fields = [
        "user__first_name",
        "user__last_name",
        "specialization",
        "user__email",
        "license_number",
    ]

    filterset_fields = [
        "department",
    ]

    def perform_create(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can create doctor profiles."
            )
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can update doctor profiles."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can delete doctor profiles."
            )
        instance.delete()

