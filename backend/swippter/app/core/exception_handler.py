import json
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from app.utilities.utilities import FILLER as F

class ExceptionHandler(MiddlewareMixin):
    pass

def Exception404(request, *args, **argv):
    payload = {F.CODE: status.HTTP_404_NOT_FOUND, F.MESSAGE: F.REQUEST_URL_NOT_FOUND}
    response = HttpResponse(
        json.dumps(payload),
        content_type=F.APPLICATION_JSON,
        status=status.HTTP_404_NOT_FOUND,
    )
    return response

def Exception500(request, *args, **argv):
    payload = {
        F.CODE: status.HTTP_500_INTERNAL_SERVER_ERROR,
        F.MESSAGE: F.INTERNAL_SERVER_ERROR,
    }
    response = HttpResponse(
        json.dumps(payload),
        content_type=F.APPLICATION_JSON,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return response
