from django.urls import path
from app.views.authentication_views import SignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("api/v1/signup", SignupView.as_view(), name="signup"),
    path("api/v1/login", SignupView.as_view(), name="index"),
    path("api/v1/logout", SignupView.as_view(), name="index"),
    path("api/v1/refresh", SignupView.as_view(), name="index"),
    path("api/v1/forgot", SignupView.as_view(), name="index"),
    path("api/v1/change-password", SignupView.as_view(), name="index"),
    path("api/v1/verify/<uidb64>/<token>", SignupView.as_view(), name="index"),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]