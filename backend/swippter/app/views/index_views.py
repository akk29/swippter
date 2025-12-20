from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from rest_framework import status as S
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.core.exceptions import (
    UnprocessableError,
    CUSTOM_CODE,
    ExceptionGenerator
)
from app.utils.utilities import (
    F,
    get_http_response,
    my_etag_func,
    my_last_modified_func,
)
from app.core.throttlers import CustomRateThrottle

class IndexView(APIView):

    throttle_classes = [UserRateThrottle]

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
        errors = ExceptionGenerator.error_generator(
            [
                {
                    F.FIELD: F.USERNAME,
                    F.ERRORS: [
                        {
                            F.CODE: CUSTOM_CODE.USERNAME_TAKEN,
                            F.MSG: F.USERNAME_UNAVAILABLE,
                        },
                        {
                            F.CODE: CUSTOM_CODE.USERNAME_NOT_ALLOWED,
                            F.MSG: F.USERNAME_NOT_ALLOWED,
                        },
                    ],
                },
                {
                    F.FIELD: F.METHOD,
                    F.ERRORS: [
                        {
                            F.CODE: CUSTOM_CODE.USERNAME_TAKEN,
                            F.MSG: F.USERNAME_UNAVAILABLE,
                        },
                        {
                            F.CODE: CUSTOM_CODE.USERNAME_NOT_ALLOWED,
                            F.MSG: F.USERNAME_NOT_ALLOWED,
                        },
                    ],
                },
                {
                    F.FIELD: F.APPLICATION_JSON,
                    F.ERRORS: [
                        {
                            F.CODE: CUSTOM_CODE.USERNAME_TAKEN,
                            F.MSG: F.USERNAME_UNAVAILABLE,
                        },
                        {
                            F.CODE: CUSTOM_CODE.USERNAME_NOT_ALLOWED,
                            F.MSG: F.USERNAME_NOT_ALLOWED,
                        },
                    ],
                },
            ]
        )
        raise UnprocessableError(
            code=S.HTTP_422_UNPROCESSABLE_ENTITY, msg=F.UNPROCESSABLE, errors=errors
        )
