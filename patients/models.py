from django.db import models
from accounts.models import User


class Patient(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES
    )

    address = models.TextField()

    emergency_contact = models.JSONField(
        default=dict,
        blank=True
    )

    insurance_provider = models.CharField(
        max_length=255,
        blank=True
    )

    insurance_details = models.TextField(
        blank=True
    )

    allergies = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.email