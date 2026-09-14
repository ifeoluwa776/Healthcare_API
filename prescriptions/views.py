from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
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

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "medical_record",
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