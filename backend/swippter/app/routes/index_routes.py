from django.urls import path
from app.views.index_views import IndexView, ErrorView, RaiseErrorView

urlpatterns = [
    path("api/v1/", IndexView.as_view(), name="index"),
    path("api/v1/error/<code>", ErrorView.as_view(), name="error"),
    path("api/v1/raise-error", RaiseErrorView.as_view(), name="raise-error"),
]
