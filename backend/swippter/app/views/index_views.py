from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.utils.utilities import F, get_http_response
from app.core.exceptions import MethodNotAllowedError

class IndexView(APIView):

    throttle_classes = [UserRateThrottle]

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

    def head(self, request):
        response = get_http_response(
            {F.VERSION: F.V1, F.METHOD: request.method}, status.HTTP_200_OK
        )
        return response
    
class ErrorView(APIView):

    throttle_classes = [UserRateThrottle]

    def get(self, request, code):
        payload = {
            F.STATUS: code,
            F.NAME: F.ERRORS,
            F.CODE: code,
            F.MSG: F.ERRORS,
            F.ERRORS: [],
        }
        response = get_http_response(payload, code)
        return response


class RaiseErrorView(APIView):

    throttle_classes = [UserRateThrottle]

    def get(self, request):        
        raise MethodNotAllowedError()