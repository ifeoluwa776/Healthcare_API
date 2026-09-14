from django.db import models
from django.core.validators import FileExtensionValidator

from patients.models import Patient
from doctors.models import Doctor


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_records"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="medical_records"
    )

    diagnosis = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    consultation_notes = models.TextField(blank=True)

    attachments = models.FileField(
        upload_to="medical_record_attachments/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "jpg",
                    "jpeg",
                    "png",
                ]
            )
        ]
    )

    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.diagnosis[:30]}"

