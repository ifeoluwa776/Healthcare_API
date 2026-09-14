from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.select_related(
        "patient",
        "doctor"
    ).all()

    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "patient",
        "doctor",
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return self.queryset

        if user.role == "doctor":
            return self.queryset.filter(
                doctor__user=user
            )

        if user.role == "patient":
            return self.queryset.filter(
                patient__user=user
            )

        return self.queryset.none()

    def perform_create(self, serializer):
        if self.request.user.role != "doctor":
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Only doctors can create medical records."
            )

        serializer.save(
            doctor=self.request.user.doctor_profile
        )