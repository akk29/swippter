from django.urls import path
from app.views.index_views import IndexView

urlpatterns = [
    path('api/v1/', IndexView.as_view(),name='index'),
]