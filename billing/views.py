from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer


class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Invoice.objects.all()

        if user.role == "patient":
            return Invoice.objects.filter(patient__user=user)

        return Invoice.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can create invoices."
            )

        serializer.save()


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Payment.objects.all()

        if user.role == "patient":
            return Payment.objects.filter(patient__user=user)

        return Payment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "admin":
            serializer.save()
            return

        if user.role != "patient":
            raise PermissionDenied(
                "You do not have permission to create payments."
            )

        invoice = serializer.validated_data.get("invoice")

        if invoice is None or invoice.patient.user != user:
            raise PermissionDenied(
                "You can only make payments for your own invoices."
            )

        serializer.save(patient=invoice.patient)

