from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.core.exceptions import UnprocessableError, CUSTOM_CODE
from app.utils.utilities import (
    F,
    get_http_response,
    my_etag_func,
    my_last_modified_func,
)


class IndexView(APIView):

    throttle_classes = [UserRateThrottle]

    @method_decorator(
        condition(etag_func=my_etag_func, last_modified_func=my_last_modified_func),
        name="dispatch",
    )
    def get(self, request):
        response = get_http_response(
            {F.VERSION: F.V1, F.METHOD: request.method}, status.HTTP_200_OK
        )
        return response

    def post(self, request):
        response = get_http_response(
            {F.VERSION: F.V1, F.METHOD: request.method}, status.HTTP_200_OK
        )
        return response

    def put(self, request):
        response = get_http_response(
            {F.VERSION: F.V1, F.METHOD: request.method}, status.HTTP_200_OK
        )
        return response

    def patch(self, request):
        response = get_http_response(
            {F.VERSION: F.V1, F.METHOD: request.method}, status.HTTP_200_OK
        )
        return response

    def delete(self, request):
        response = get_http_response(
            {F.VERSION: F.V1, F.METHOD: request.method}, status.HTTP_200_OK
        )
        return response


class RaiseErrorView(APIView):

    throttle_classes = [UserRateThrottle]

    def get(self, request):
        raise UnprocessableError(
            errors=[
                {
                    F.FIELD: F.USERNAME,
                    F.CODE: CUSTOM_CODE.USERNAME_TAKEN,
                    F.MSG: F.USERNAME_UNAVAILABLE,
                }
            ]
        )
