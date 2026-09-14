from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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
            return Review.objects.filter(
                patient__user=user
            )

        return Review.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "patient":
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only patients can create reviews."
            )

        serializer.save(
            patient=self.request.user.patient_profile
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="doctor/(?P<doctor_id>[^/.]+)/average-rating",
    )
    def average_rating(self, request, doctor_id=None):
        reviews = Review.objects.filter(
            doctor_id=doctor_id
        )

        average = reviews.aggregate(
            average_rating=Avg("rating")
        )["average_rating"]

        return Response({
            "doctor": int(doctor_id),
            "average_rating": round(float(average), 2)
            if average is not None
            else 0,
            "total_reviews": reviews.count(),
        })