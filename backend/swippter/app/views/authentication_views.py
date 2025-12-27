from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.core.throttlers import CustomRateThrottle
from app.pattern.factory.service_factory import ServiceFactory
from app.utils.utilities import (
    F,
    get_http_response,
    my_etag_func,
    my_last_modified_func,
)

auth_service = ServiceFactory.get_authentication_service()

class SignupView(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        payload = auth_service.signup_service()
        response = get_http_response(payload=payload)
        return response