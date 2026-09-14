from django.urls import path
from .views import (
    ProfileView,
    RegisterView,
    UserListView,
    LoginView,
    LogoutView,
    PasswordResetView,
    EmailVerificationView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="users"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset-password/", PasswordResetView.as_view(), name="password_reset"),
    path("verify-email/", EmailVerificationView.as_view(), name="verify_email"),
]

