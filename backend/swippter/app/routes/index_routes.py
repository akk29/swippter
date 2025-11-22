from django.urls import path
from app.views.index_views import IndexView, RaiseErrorView

urlpatterns = [
    path("api/v1/", IndexView.as_view(), name="index"),
    path("api/v1/raise-error", RaiseErrorView.as_view(), name="raise-error"),
]
