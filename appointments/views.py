from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    DateFilter,
)

from .models import Appointment
from .serializers import AppointmentSerializer
from notifications.models import Notification
from notifications.services import send_notification_email


class AppointmentFilter(FilterSet):
    appointment_date = DateFilter(
        field_name="appointment_date",
        lookup_expr="date",
    )

    appointment_date_after = DateFilter(
        field_name="appointment_date",
        lookup_expr="date__gte",
    )

    appointment_date_before = DateFilter(
        field_name="appointment_date",
        lookup_expr="date__lte",
    )

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "doctor",
            "status",
            "appointment_date",
        ]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related(
        "patient",
        "doctor"
    ).all()

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_class = AppointmentFilter

    search_fields = [
        "reason",
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
        user = self.request.user

        if user.role not in [
            "admin",
            "doctor",
            "patient",
        ]:
            raise PermissionDenied(
                "You do not have permission to create appointments."
            )

        serializer.save()

    @action(
        detail=True,
        methods=["post"],
        url_path="remind",
    )
    def remind(self, request, pk=None):
        appointment = self.get_object()

        notification = Notification.objects.create(
            user=appointment.patient.user,
            title="Appointment Reminder",
            message=(
                f"You have an appointment with Dr. "
                f"{appointment.doctor.user.first_name} "
                f"{appointment.doctor.user.last_name} "
                f"on {appointment.appointment_date}."
            ),
            notification_type="appointment",
        )

        send_notification_email(notification)

        return Response({
            "message": "Appointment reminder sent successfully.",
            "notification_id": notification.id,
        })