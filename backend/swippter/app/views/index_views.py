from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.core.throttlers import CustomRateThrottle
from app.pattern.factory.service_factory import ServiceFactory
from app.utils.utilities import (
    F,
    get_http_response,
    my_etag_func,
    my_last_modified_func,
)

index_service = ServiceFactory.get_index_service()

class IndexView(APIView):

    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @method_decorator(
        condition(etag_func=my_etag_func, last_modified_func=my_last_modified_func),
        name="dispatch",
    )
    def get(self, request):
        response = get_http_response({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def post(self, request):
        response = get_http_response({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def put(self, request):
        response = get_http_response({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def patch(self, request):
        response = get_http_response({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def delete(self, request):
        response = get_http_response({F.VERSION: F.V1, F.METHOD: request.method})
        return response


class RaiseErrorView(APIView):

    throttle_classes = [CustomRateThrottle]

    def post(self, request):
        return index_service.raise_error_service()