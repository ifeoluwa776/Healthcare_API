from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LaboratoryRequestViewSet,
    LaboratoryResultViewSet,
)

router = DefaultRouter()

router.register(
    r"requests",
    LaboratoryRequestViewSet,
    basename="laboratory-request"
)

router.register(
    r"results",
    LaboratoryResultViewSet,
    basename="laboratory-result"
)

urlpatterns = [
    path("", include(router.urls)),
]