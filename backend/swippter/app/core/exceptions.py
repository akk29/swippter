from django.db import DatabaseError
from rest_framework import status as S
from rest_framework.exceptions import (
    APIException as DRF_APIException,
    Throttled as DRF_Throttled,
)
from rest_framework.views import exception_handler
from rest_framework.response import Response
from app.core.logging import Logger
from app.utils.utilities import F, get_http_response, generate_random_string, get_item
from app.core.errors import (
    JWT_ERRORS_MAP,
    DRF_EXCEPTION_MAP,
    DB_ERROR_MAP,
    EXCEPTION_ERROR_MAP,
    ERROR_NAME,
)

logger = Logger.get_logger()


def process_library_exceptions(exc, context):
    response = exception_handler(exc, context)

    """ rest_framework_simplejwt related error interception """
    if any([True for _ in JWT_ERRORS_MAP.keys() if type(exc) == _]):
        payload = JWT_ERRORS_MAP[type(exc)]
        response = Response(payload, status=payload[F.STATUS])
        return response

    """ django-rest-framework error interception """
    if isinstance(exc, DRF_APIException):
        if isinstance(exc, DRF_Throttled):
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
        payload = DRF_EXCEPTION_MAP[type(exc)]
        response = get_http_response(payload, payload[F.STATUS])
        return response

    if isinstance(exc, DatabaseError):
        for exc_type, config in DB_ERROR_MAP.items():
            if isinstance(exc, exc_type):
                payload = {
                    F.STATUS: config[F.STATUS],
                    F.NAME: config[F.NAME],
                    F.CODE: config[F.CODE],
                    F.MSG: config[F.MSG],
                    F.ERRORS: [],
                }
                response = get_http_response(payload, payload[F.STATUS])
                return response

    """ Django internal error interception"""
    if any([True for _ in EXCEPTION_ERROR_MAP.keys() if type(exc) == _]):
        payload = EXCEPTION_ERROR_MAP[type(exc)]
        response.data = payload
        return response

    """ System Defined Error Handling """
    payload = ExceptionGenerator.process_exception(exc)
    response = get_http_response(payload, payload[F.STATUS])
    return response


class ExceptionGenerator:

    @staticmethod
    def process_exception(error):
        """This method helps to create response structure from Custom Error Neatly
        app.core.middleware.JSONValidationMiddleware
        exception = UnprocessableError(errors=[{F.BODY: F.INVALID_JSON}])
        payload = ExceptionGenerator.process_exception(exception)
        response = get_http_response(payload, payload[F.STATUS])
        return response
        """
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
        self.code = get_item(args, 0) or kwargs.pop(
            F.CODE, S.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.name = kwargs.pop(F.NAME, ERROR_NAME.INTERNAL_SERVER_ERROR)
        self.msg = get_item(args, 1) or kwargs.pop(F.MSG, F.INTERNAL_SERVER_ERROR)
        self.errors = get_item(args, 2) or kwargs.pop(F.ERRORS, [])
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


class ConflitError(BaseError):

    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_409_CONFLICT,
            F.CODE: S.HTTP_409_CONFLICT,
            F.NAME: ERROR_NAME.CONFLICT_ERROR,
            F.MSG: F.CONFLICT,
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


class ServiceUnavailableError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_503_SERVICE_UNAVAILABLE,
            F.CODE: S.HTTP_503_SERVICE_UNAVAILABLE,
            F.NAME: ERROR_NAME.UNAVAILABLE_ERROR,
            F.MSG: F.UNAVAILABLE,
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
