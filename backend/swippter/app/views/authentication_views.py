from rest_framework import status as S
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.pattern.factory.service_factory import ServiceFactory
from app.serializers.auth_serializers import UserSerializer
from app.utils.utilities import get_http_response

auth_service = ServiceFactory.get_authentication_service()


class SignupView(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        response = auth_service.signup_service(**payload)
        serialized_data = UserSerializer(response).data
        http_response = get_http_response(
            payload=serialized_data, status=S.HTTP_201_CREATED
        )
        return http_response


class SigninView(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        response = auth_service.signin_service(**payload)
        serialized_data = UserSerializer(response).data
        http_response = get_http_response(payload=serialized_data)
        return http_response