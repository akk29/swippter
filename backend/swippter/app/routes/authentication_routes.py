from django.urls import path
from app.views.authentication_views import SignupView, SigninView, ForgotView, VerifyTokenView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

urlpatterns = [
    path("api/v1/signup", SignupView.as_view(), name="signup"),
    path("api/v1/signin", SigninView.as_view(), name="signin"),
    path("api/v1/signout", TokenBlacklistView.as_view(), name="signout"),
    path("api/v1/refresh", TokenRefreshView.as_view(), name="refresh"),
    path("api/v1/verify", TokenVerifyView.as_view(), name="verify"),
    path("api/v1/forgot", ForgotView.as_view(), name="forgot"),
    path("api/v1/verify-token/<uidb64>/<token>", VerifyTokenView.as_view(), name="verify-token"),
    path("api/v1/change-password", ChangePasswordView.as_view(), name="change-password"),
]
