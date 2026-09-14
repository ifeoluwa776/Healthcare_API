from django.db import models
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor


class LaboratoryRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Requested"),
        ("sample_collected", "Sample Collected"),
        ("in_progress", "In Progress"),
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

    laboratory_technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_laboratory_requests",
        limit_choices_to={"role": "lab_technician"},
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

    report = models.FileField(
        upload_to="laboratory_reports/",
        blank=True,
        null=True
    )

    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.laboratory_request.test_name}"