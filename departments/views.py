from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can create departments."
            )
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can update departments."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can delete departments."
            )
        instance.delete()

