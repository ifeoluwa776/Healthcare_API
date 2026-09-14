from django.utils import timezone
from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ["id", "created_at", "status"]

    def validate_appointment_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Appointment cannot be booked in the past."
            )
        return value

    def validate(self, attrs):
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")

        if not patient:
            raise serializers.ValidationError(
                {"patient": "Patient is required."}
            )

        if not doctor:
            raise serializers.ValidationError(
                {"doctor": "Doctor is required."}
            )

        return attrs