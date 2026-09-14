from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/accounts/", include("accounts.urls")),
    path("api/departments/", include("departments.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/appointments/", include("appointments.urls")),
    path("api/medical-records/", include("medical_records.urls")),
    path("api/prescriptions/", include("prescriptions.urls")),
    path("api/laboratory/", include("laboratory.urls")),
    path("api/billing/", include("billing.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/analytics/", include("analytics.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)