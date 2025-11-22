import json
import hashlib
from datetime import datetime
from django.http import HttpResponse

class FILLER:
    APPLICATION_JSON = "application/json"
    CODE = "code"
    METHOD = "method"
    MESSAGE = "message"
    MSG = "msg"
    NAME = "name"
    STATUS = "status"
    VERSION = "version"
    V1 = "v1"
    ERRORS = "errors"
    FIELD = "field"
    USERNAME = "username"

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

F = FILLER

def get_http_response(payload=None, status=None,content_type=None):
    response = HttpResponse(
        json.dumps(payload), status=status, content_type=F.APPLICATION_JSON
    )
    return response

def my_etag_func(request, **kwargs):
    return hashlib.sha256(f"fixed".encode()).hexdigest()

def my_last_modified_func(request, **kwargs):
    return datetime(2024, 1, 1, 12, 0)