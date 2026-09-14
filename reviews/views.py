from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    search_fields = ["feedback"]
    filterset_fields = ["rating", "doctor", "patient"]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Review.objects.all()

        if user.role == "patient":
            return Review.objects.filter(patient__user=user)

        return Review.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "patient":
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Only patients can create reviews."
            )

        serializer.save(patient=self.request.user.patient_profile)