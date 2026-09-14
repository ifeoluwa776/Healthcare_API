from django.db import models
from accounts.models import User
from departments.models import Department


class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    specialization = models.CharField(max_length=100)

    license_number = models.CharField(
        max_length=100,
        unique=True
    )
    license_file = models.FileField(
        upload_to="doctor_licenses/",
        blank=True,
        null=True
    )

    years_of_experience = models.PositiveIntegerField(
        default=0
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    availability = models.JSONField(
        default=dict,
        blank=True
    )

    profile_photo = models.ImageField(
        upload_to="doctor_profiles/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"