from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "gender",
        "blood_group",
        "date_of_birth",
    )

    search_fields = (
        "user__email",
    )

    list_filter = (
        "gender",
        "blood_group",
    )