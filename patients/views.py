from rest_framework import viewsets

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__phone_number",
    ]

    filterset_fields = [
        "blood_group",
        "gender",
    ]
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__phone_number",
    ]

    filterset_fields = [
        "blood_group",
        "gender",
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return self.queryset

        if user.role == "patient":
            return self.queryset.filter(user=user)

        if user.role in [
            "doctor",
            "nurse",
            "receptionist",
            "lab_technician",
        ]:
            return self.queryset

        return self.queryset.none()

    def perform_create(self, serializer):
        if self.request.user.role not in ["admin", "receptionist"]:
            raise PermissionDenied(
                "Only administrators or receptionists can create patient profiles."
            )
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user

        if user.role not in ["admin", "receptionist"]:
            raise PermissionDenied(
                "Only administrators or receptionists can update patient profiles."
            )

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can delete patient profiles."
            )

        instance.delete()

