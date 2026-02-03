from django.core.cache import cache
from django.db import connection
from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from app.core.throttlers import CustomRateThrottle
from app.pattern.factory.service_factory import ServiceFactory
from app.utils.utilities import (
    F,
    get_http_response_msg,
    my_etag_func,
    my_last_modified_func,
)

index_service = ServiceFactory.get_index_service()

class HealthCheckView(APIView):

    def get(self, request):
        health_status = {
            F.VERSION: F.V1,
            F.METHOD: request.method,
            F.STATUS: F.HEALTHY,
            F.DATABASE: F.UNKNOWN,
            F.REDIS: F.UNKNOWN,
        }

        try:
            connection.ensure_connection()
            health_status[F.DATABASE] = F.CONNECTED
        except Exception as e:
            health_status[F.DATABASE] = "{} : {}".format(F.ERROR,str(e))
            health_status[F.STATUS] = F.UNHEALTHY

        try:
            cache.set(F.HEALTH_CHECK, F.OK, 10)
            if cache.get(F.HEALTH_CHECK) == F.OK:
                health_status[F.REDIS] = F.CONNECTED
            else:
                health_status[F.REDIS] = F.ERROR
                health_status[F.STATUS] = F.UNHEALTHY
        except Exception as e:
            health_status[F.REDIS] = "{} : {}".format(F.ERROR,str(e))
            health_status[F.STATUS] = F.UNHEALTHY

        response = get_http_response_msg(payload=health_status)
        return response


class IndexView(APIView):

    @method_decorator(
        condition(etag_func=my_etag_func, last_modified_func=my_last_modified_func),
        name="dispatch",
    )
    def get(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def post(self, request):
        response = get_http_response_msg(
            {F.VERSION: F.V1, F.METHOD: request.method}, message=F.CREATED
        )
        return response

    def put(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def patch(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def delete(self, request):
        response = get_http_response_msg(
            {F.VERSION: F.V1, F.METHOD: request.method}, message=F.DELETED
        )
        return response


class RaiseErrorView(APIView):

    throttle_classes = [CustomRateThrottle]

    def post(self, request):
        return index_service.raise_error_service()
