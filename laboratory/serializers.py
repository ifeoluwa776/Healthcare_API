from rest_framework import serializers
from .models import LaboratoryRequest, LaboratoryResult


class LaboratoryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryRequest
        fields = [
            "id",
            "patient",
            "doctor",
            "test_name",
            "description",
            "status",
            "requested_at",
        ]
        read_only_fields = ["id", "requested_at"]


class LaboratoryResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryResult
        fields = [
            "id",
            "laboratory_request",
            "result",
            "notes",
            "completed_at",
        ]
        read_only_fields = ["id", "completed_at"]