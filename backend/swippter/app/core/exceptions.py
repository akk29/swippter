from django.utils.deprecation import MiddlewareMixin
from rest_framework import status as S
from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler
from app.core.logging import Logger
from app.utils.utilities import F, get_http_response, generate_random_string

class ERROR_NAME:
    BAD_REQUEST_ERROR = "BAD_REQUEST_ERROR"
    FORBIDDEN_ERROR = "FORBIDDEN_ERROR"
    METHOD_NOT_ALLOWED_ERROR = "METHOD_NOT_ALLOWED_ERROR"
    NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
    UNAUTHORIZED_ERROR = "UNAUTHORIZED_ERROR"
    UNPROCESSABLE_ERROR = "UNPROCESSABLE_ERROR"
    TOO_MANY_REQUESTS_ERROR = "TOO_MANY_REQUESTS_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


# Application / Business Logic Based Errors
class CUSTOM_CODE:
    EMAIL_MUST_BE_SET = "2886623e"
    USERNAME_TAKEN = "428e5342"
    USERNAME_NOT_ALLOWED = "09023859"

def process_library_exceptions(exc, context):
    response = exception_handler(exc, context)    

    if isinstance(exc, Throttled):
        wait_time = exc.wait
        payload = {
            F.STATUS: S.HTTP_429_TOO_MANY_REQUESTS,
            F.NAME: ERROR_NAME.TOO_MANY_REQUESTS_ERROR,
            F.CODE: S.HTTP_429_TOO_MANY_REQUESTS,
            F.MSG: F.TOO_MANY_REQUESTS.format(wait_time),
            F.ERRORS: [],
        }
        response = get_http_response(payload, payload[F.STATUS])
    return response


class ExceptionHandler(MiddlewareMixin):
    def process_exception(self, request, exception):
        payload = ExceptionGenerator.process_exception(exception)
        response = get_http_response(payload, payload[F.STATUS])
        return response


class ExceptionGenerator:

    @staticmethod
    def process_exception(error):
        return {
            F.STATUS: error.status,
            F.NAME: error.name,
            F.CODE: error.code,
            F.MSG: error.msg,
            F.ERRORS: error.errors,
        }

    # to generate error and key clubbing for frontend purpose
    @staticmethod
    def error_generator(code_and_messages=[]):
        group_keys_map = {
            _[F.FIELD]: generate_random_string() for _ in code_and_messages
        }
        error_keys = []
        [
            error_keys.extend(
                [
                    {
                        F.FIELD: _[F.FIELD],
                        F.CODE: __[F.CODE],
                        F.KEY: group_keys_map[_[F.FIELD]],
                        F.MSG: __[F.MSG],
                    }
                    for __ in _[F.ERRORS]
                ]
            )
            for _ in code_and_messages
        ]
        return error_keys


class BaseError(Exception):

    def __init__(self, *args, **kwargs):
        self.status = kwargs.pop(F.STATUS, S.HTTP_500_INTERNAL_SERVER_ERROR)
        self.code = args[0] or kwargs.pop(F.CODE, S.HTTP_500_INTERNAL_SERVER_ERROR)
        self.name = kwargs.pop(F.NAME, ERROR_NAME.INTERNAL_SERVER_ERROR)
        self.msg = args[1] or kwargs.pop(F.MSG, F.INTERNAL_SERVER_ERROR)
        self.errors = args[2] or kwargs.pop(F.ERRORS, [])
        self.logger = Logger.log_exception(self)
        super().__init__(self.msg)

    def __process_exception__(self):
        return {
            F.STATUS: self.status,
            F.NAME: self.name,
            F.CODE: self.code,
            F.MSG: self.msg,
            F.ERRORS: self.errors,
        }


class BadRequestError(BaseError):

    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_400_BAD_REQUEST,
            F.CODE: S.HTTP_400_BAD_REQUEST,
            F.NAME: ERROR_NAME.BAD_REQUEST_ERROR,
            F.MSG: F.BAD_REQUEST,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class UnauthorizedError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_401_UNAUTHORIZED,
            F.CODE: S.HTTP_401_UNAUTHORIZED,
            F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
            F.MSG: F.UNAUTHORIZED,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class ForbiddenError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_403_FORBIDDEN,
            F.CODE: S.HTTP_403_FORBIDDEN,
            F.NAME: ERROR_NAME.FORBIDDEN_ERROR,
            F.MSG: F.FORBIDDEN,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class NotFoundError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_404_NOT_FOUND,
            F.CODE: S.HTTP_404_NOT_FOUND,
            F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
            F.MSG: F.NOT_FOUND,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class MethodNotAllowedError(BaseError):

    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_405_METHOD_NOT_ALLOWED,
            F.CODE: S.HTTP_405_METHOD_NOT_ALLOWED,
            F.NAME: ERROR_NAME.METHOD_NOT_ALLOWED_ERROR,
            F.MSG: F.METHOD_NOT_ALLOWED,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class UnprocessableError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_422_UNPROCESSABLE_ENTITY,
            F.CODE: S.HTTP_422_UNPROCESSABLE_ENTITY,
            F.NAME: ERROR_NAME.UNPROCESSABLE_ERROR,
            F.MSG: F.UNPROCESSABLE,
        }
        super().__init__(*[code, msg, errors], **kwargs)


def Exception404(request, *args, **kwargs):
    payload = {
        F.STATUS: S.HTTP_404_NOT_FOUND,
        F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
        F.CODE: S.HTTP_404_NOT_FOUND,
        F.MSG: F.NOT_FOUND,
        F.ERRORS: [],
    }
    response = get_http_response(payload, S.HTTP_404_NOT_FOUND)
    return response


def Exception500(request, *args, **kwargs):
    payload = {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    }
    response = get_http_response(payload, S.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
