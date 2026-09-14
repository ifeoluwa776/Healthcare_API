from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "department",
        "specialization",
        "license_number",
        "years_of_experience",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "license_number",
    )
    list_filter = (
        "department",
        "specialization",
    )