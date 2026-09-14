from django.urls import path
from .views import (
    InvoiceListCreateView,
    PaymentListCreateView,
)

urlpatterns = [
    path("invoices/", InvoiceListCreateView.as_view(), name="invoice-list"),
    path("payments/", PaymentListCreateView.as_view(), name="payment-list"),
]