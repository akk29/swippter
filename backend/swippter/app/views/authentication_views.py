from rest_framework import status as S
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.pattern.factory.service_factory import ServiceFactory
from app.serializers.auth_serializers import UserSerializer, ForgotSerializer
from app.utils.utilities import get_http_response_msg, F

auth_service = ServiceFactory.get_authentication_service()
class SignupView(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        response = auth_service.signup_service(**payload)
        serialized_data = UserSerializer(response).data
        http_response = get_http_response_msg(
            payload=serialized_data, status=S.HTTP_201_CREATED, message=F.CREATED
        )
        return http_response

class SigninView(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        response = auth_service.signin_service(**payload)
        serialized_data = UserSerializer(response).data
        http_response = get_http_response_msg(payload=serialized_data)
        return http_response

class ForgotView(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        payload = JSONParser().parse(request)
        auth_service.forgot_service(**payload)
        http_response = get_http_response_msg()
        return http_response

class VerifyTokenView(APIView):

    throttle_classes = [UserRateThrottle]

    def get(self, request, uidb64, token):
        response = auth_service.verify_token_service(
            **{F.UIDB64: uidb64, F.TOKEN: token}
        )
        serialized_data = ForgotSerializer(response).data
        http_response = get_http_response_msg(payload=serialized_data)
        return http_response

class ChangePasswordView(APIView):

    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = JSONParser().parse(request)
        auth_service.change_password_service(request.user,**payload)        
        http_response = get_http_response_msg()
        return http_response