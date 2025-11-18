from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.utils.utilities import F, get_http_response

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

    def options(self, request):
        response = get_http_response(
            {F.VERSION: F.V1, F.METHOD: request.method}, status.HTTP_200_OK
        )
        return response


class ErrorView(APIView):

    throttle_classes = [UserRateThrottle]

    def get(self, request, code):
        response = get_http_response({F.CODE: code}, code)
        return response
