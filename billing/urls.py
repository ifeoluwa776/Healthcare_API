from django.urls import path

from .views import (
    InvoiceListCreateView,
    PaymentListCreateView,
    PaymentReceiptView,
)

urlpatterns = [
    path(
        "invoices/",
        InvoiceListCreateView.as_view(),
        name="invoice-list"
    ),

    path(
        "payments/",
        PaymentListCreateView.as_view(),
        name="payment-list"
    ),

    path(
        "payments/<int:payment_id>/receipt/",
        PaymentReceiptView.as_view(),
        name="payment-receipt"
    ),
]