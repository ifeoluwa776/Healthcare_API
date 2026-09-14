from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related(
        "patient",
        "doctor"
    ).all()

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = [
        "patient",
        "doctor",
        "status",
    ]

    search_fields = [
        "reason",
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return self.queryset

        if user.role == "doctor":
            return self.queryset.filter(doctor__user=user)

        if user.role == "patient":
            return self.queryset.filter(patient__user=user)

        return self.queryset.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in ["admin", "doctor", "patient"]:
            raise PermissionDenied(
                "You do not have permission to create appointments."
            )

        serializer.save()

