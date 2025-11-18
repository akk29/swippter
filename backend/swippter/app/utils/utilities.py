import json
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
    ERRORS = "ERRORS"

    # Errors msgs
    BAD_REQUEST= "Bad Request"
    METHOD_NOT_ALLOWED = "Method not allowed"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    NOT_FOUND = "Not found"
    FORBIDDEN = "Forbidden"
    UNAUTHORIZED = "Unauthorized"
    UNPROCESSABLE = "Unprocessable"

F = FILLER

def get_http_response(payload=None, status=None,content_type=None):
    response = HttpResponse(
        json.dumps(payload), status=status, content_type=F.APPLICATION_JSON
    )
    return response
