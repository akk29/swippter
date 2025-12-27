from django.urls import path
from app.views.authentication_views import SignupView

urlpatterns = [
    path("api/v1/signup", SignupView.as_view(), name="signup"),
    path("api/v1/login", SignupView.as_view(), name="index"),
    path("api/v1/logout", SignupView.as_view(), name="index"),
    path("api/v1/refresh", SignupView.as_view(), name="index"),
    path("api/v1/forgot", SignupView.as_view(), name="index"),
    path("api/v1/change-password", SignupView.as_view(), name="index"),
    path("api/v1/verify/<uidb64>/<token>", SignupView.as_view(), name="index"),
]
