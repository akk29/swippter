import json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from app.utilities.utilities import FILLER as F

class IndexView(APIView):

    throttle_classes = [UserRateThrottle]

    def get(self, request):
        response = HttpResponse(
            json.dumps({F.VERSION: F.V1, F.METHOD: request.method}),
            content_type=F.APPLICATION_JSON,
            status=status.HTTP_200_OK,
        )
        return response

    def post(self, request):
        response = HttpResponse(
            json.dumps({F.VERSION: F.V1, F.METHOD: request.method}),
            content_type=F.APPLICATION_JSON,
            status=status.HTTP_200_OK,
        )
        return response

    def put(self, request):
        response = HttpResponse(
            json.dumps({F.VERSION: F.V1, F.METHOD: request.method}),
            content_type=F.APPLICATION_JSON,
            status=status.HTTP_200_OK,
        )
        return response

    def patch(self, request):
        response = HttpResponse(
            json.dumps({F.VERSION: F.V1, F.METHOD: request.method}),
            content_type=F.APPLICATION_JSON,
            status=status.HTTP_200_OK,
        )
        return response

    def delete(self, request):
        response = HttpResponse(
            json.dumps({F.VERSION: F.V1, F.METHOD: request.method}),
            content_type=F.APPLICATION_JSON,
            status=status.HTTP_200_OK,
        )
        return response

    def head(self, request):
        response = HttpResponse(
            json.dumps({F.VERSION: F.V1, F.METHOD: request.method}),
            content_type=F.APPLICATION_JSON,
            status=status.HTTP_200_OK,
        )
        return response

    def options(self, request):
        response = HttpResponse(
            json.dumps({F.VERSION: F.V1, F.METHOD: request.method}),
            content_type=F.APPLICATION_JSON,
            status=status.HTTP_200_OK,
        )
        return response


class ErrorView(APIView):

    throttle_classes = [UserRateThrottle]

    def get(self,request,code):               
        response = HttpResponse(
            json.dumps({F.CODE: code}),
            content_type=F.APPLICATION_JSON,
            status=code,
        )
        return response