from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class LaboratoryRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="laboratory_requests"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="laboratory_requests"
    )

    test_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} - {self.patient}"


class LaboratoryResult(models.Model):
    laboratory_request = models.OneToOneField(
        LaboratoryRequest,
        on_delete=models.CASCADE,
        related_name="result"
    )

    result = models.TextField()
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.laboratory_request.test_name}"