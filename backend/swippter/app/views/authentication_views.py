from rest_framework import status as S
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from app.core.throttlers import CustomRateThrottle
from app.pattern.factory.service_factory import ServiceFactory
from app.serializers.auth_serializers import UserSerializer, ForgotSerializer
from app.utils.utilities import get_http_response_msg, F
from app.views.base_api_view import BaseAPIView
from django.core.exceptions import PermissionDenied
auth_service = ServiceFactory.get_authentication_service()
class SignupView(BaseAPIView):

    throttle_classes = [CustomRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        response = auth_service.signup_service(**payload)
        serialized_data = UserSerializer(response).data
        http_response = get_http_response_msg(
            payload=serialized_data, status=S.HTTP_201_CREATED, message=F.CREATED
        )
        return http_response

class SigninView(BaseAPIView):

    throttle_classes = [CustomRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        response = auth_service.signin_service(**payload)
        serialized_data = UserSerializer(response).data
        http_response = get_http_response_msg(payload=serialized_data)
        return http_response

class ForgotView(BaseAPIView):

    throttle_classes = [CustomRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        auth_service.forgot_service(**payload)
        http_response = get_http_response_msg()
        return http_response

class VerifyTokenView(BaseAPIView):

    throttle_classes = [CustomRateThrottle]

    def get(self, request, uidb64, token):
        response = auth_service.verify_token_service(
            **{F.UIDB64: uidb64, F.TOKEN: token}
        )
        serialized_data = ForgotSerializer(response).data
        http_response = get_http_response_msg(payload=serialized_data)
        return http_response

class ChangePasswordView(BaseAPIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        auth_service.change_password_service(request.user,**payload)        
        http_response = get_http_response_msg()
        return http_response