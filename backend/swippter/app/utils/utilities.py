import json
import hashlib
import random
from datetime import datetime
from django.http import HttpResponse
from rest_framework import status as S
class FILLER:
    APPLICATION_JSON = "application/json"
    CODE = "code"
    ERRORS = "errors"
    FIELD = "field"
    KEY = "key"
    METHOD = "method"
    MESSAGE = "message"
    MSG = "msg"
    NAME = "name"
    STATUS = "status"
    USERNAME = "username"
    VERSION = "version"
    V1 = "v1"

    # Errors msgs
    BAD_REQUEST= "Bad Request"
    METHOD_NOT_ALLOWED = "Method not allowed"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    NOT_FOUND = "Not found"
    FORBIDDEN = "Forbidden"
    UNAUTHORIZED = "Unauthorized"
    TOO_MANY_REQUESTS = "You have made too many requests. Please try again later. Retry after {} seconds"
    UNPROCESSABLE = "Unprocessable"

    # Custom Error msgs
    USERNAME_UNAVAILABLE = "Username unavailable"
    USERNAME_NOT_ALLOWED = "Username not allowed"

F = FILLER

def get_http_response(payload=None, status=S.HTTP_200_OK,content_type=F.APPLICATION_JSON):
    response = HttpResponse(
        json.dumps(payload), status=status, content_type=F.APPLICATION_JSON
    )
    return response

def my_etag_func(request, **kwargs):
    return hashlib.sha256(f"fixed".encode()).hexdigest()

def my_last_modified_func(request, **kwargs):
    return datetime(2024, 1, 1, 12, 0)

def generate_random_string():    
    return "".join([chr(random.randint(ord('A'),ord('Z'))) for _ in range(5)])
