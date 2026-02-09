import traceback
from django.db import DatabaseError
from rest_framework import status as S
from rest_framework.exceptions import (
    APIException as DRF_APIException,
    Throttled as DRF_Throttled,
)
from rest_framework.views import exception_handler
from app.core.logging import Logger
from app.utils.utilities import F, get_http_response, generate_random_string, get_item
from app.core.errors import (
    JWT_ERRORS_MAP,
    DRF_EXCEPTION_MAP,
    DB_ERROR_MAP,
    EXCEPTION_ERROR_MAP,
    REDIS_ERROR_MAP,
    CELERY_ERROR_MAP,
    RABBITMQ_ERROR_MAP,
    ERROR_NAME,
    CUSTOM_CODE as CC,
)

logger = Logger.get_logger()

def attach_meta_data(exc, response):
    tb_frames = traceback.extract_tb(exc.__traceback__)
    if(tb_frames):
        last_frame = tb_frames[-1]
        file_name = last_frame.filename
        line_no = last_frame.lineno
        func_name = last_frame.name
        response._exception_metadata = {
            "exception_type": exc.__class__.__name__,
            "file": file_name,
            "line": line_no,
            "function": func_name,
            "exception_repr": exc.__repr__(),
        }
    return response

def process_library_exceptions(exc, context):

    response = exception_handler(exc, context)

    """ rest_framework_simplejwt related error interception """
    if any([True for _ in JWT_ERRORS_MAP.keys() if type(exc) == _]):
        payload = JWT_ERRORS_MAP[type(exc)]
        response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
        return response

    """ Redis related error interception """
    if any([True for _ in REDIS_ERROR_MAP.keys() if type(exc) == _]):
        payload = REDIS_ERROR_MAP[type(exc)]
        response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
        return response

    """ Celery related error interception """
    if any([True for _ in CELERY_ERROR_MAP.keys() if type(exc) == _]):
        payload = CELERY_ERROR_MAP[type(exc)]
        response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
        return response

    """ Rabbitmq related error interception """
    if any([True for _ in RABBITMQ_ERROR_MAP.keys() if type(exc) == _]):
        payload = RABBITMQ_ERROR_MAP[type(exc)]
        response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
        return response

    """ django-rest-framework error interception """
    if isinstance(exc, DRF_APIException):
        if isinstance(exc, DRF_Throttled):
            wait_time = exc.wait
            payload = {
                F.STATUS: S.HTTP_429_TOO_MANY_REQUESTS,
                F.NAME: ERROR_NAME.TOO_MANY_REQUESTS_ERROR,
                F.CODE: S.HTTP_429_TOO_MANY_REQUESTS.__str__(),
                F.MSG: F.TOO_MANY_REQUESTS.format(wait_time),
                F.ERRORS: [],
            }
            response = attach_meta_data(
                exc, get_http_response(payload, payload[F.STATUS])
            )
            return response
        payload = DRF_EXCEPTION_MAP[type(exc)]
        response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
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
                response = attach_meta_data(
                    exc, get_http_response(payload, payload[F.STATUS])
                )
                return response

    """ Django internal error interception"""
    if any([True for _ in EXCEPTION_ERROR_MAP.keys() if type(exc) == _]):
        payload = EXCEPTION_ERROR_MAP[type(exc)]
        response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
        return response

    """ System Defined Error Handling"""
    if isinstance(exc, BaseError):
        payload = ExceptionGenerator.process_exception(exc)
        response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
        return response

    """ For rest of the Unhandled Error"""
    payload = {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: S.HTTP_500_INTERNAL_SERVER_ERROR.__str__(),
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    }
    response = attach_meta_data(exc, get_http_response(payload, payload[F.STATUS]))
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
            F.CODE: S.HTTP_400_BAD_REQUEST.__str__(),
            F.NAME: ERROR_NAME.BAD_REQUEST_ERROR,
            F.MSG: F.BAD_REQUEST,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class UnauthorizedError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_401_UNAUTHORIZED,
            F.CODE: S.HTTP_401_UNAUTHORIZED.__str__(),
            F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
            F.MSG: F.UNAUTHORIZED,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class ForbiddenError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_403_FORBIDDEN,
            F.CODE: S.HTTP_403_FORBIDDEN.__str__(),
            F.NAME: ERROR_NAME.FORBIDDEN_ERROR,
            F.MSG: F.FORBIDDEN,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class NotFoundError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_404_NOT_FOUND,
            F.CODE: S.HTTP_404_NOT_FOUND.__str__(),
            F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
            F.MSG: F.NOT_FOUND,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class MethodNotAllowedError(BaseError):

    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_405_METHOD_NOT_ALLOWED,
            F.CODE: S.HTTP_405_METHOD_NOT_ALLOWED.__str__(),
            F.NAME: ERROR_NAME.METHOD_NOT_ALLOWED_ERROR,
            F.MSG: F.METHOD_NOT_ALLOWED,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class ConflitError(BaseError):

    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_409_CONFLICT,
            F.CODE: S.HTTP_409_CONFLICT.__str__(),
            F.NAME: ERROR_NAME.CONFLICT_ERROR,
            F.MSG: F.CONFLICT,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class UnprocessableError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_422_UNPROCESSABLE_ENTITY,
            F.CODE: S.HTTP_422_UNPROCESSABLE_ENTITY.__str__(),
            F.NAME: ERROR_NAME.UNPROCESSABLE_ERROR,
            F.MSG: F.UNPROCESSABLE,
        }
        super().__init__(*[code, msg, errors], **kwargs)


class ServiceUnavailableError(BaseError):
    def __init__(self, code=None, msg=None, errors=None):
        kwargs = {
            F.STATUS: S.HTTP_503_SERVICE_UNAVAILABLE,
            F.CODE: S.HTTP_503_SERVICE_UNAVAILABLE.__str__(),
            F.NAME: ERROR_NAME.UNAVAILABLE_ERROR,
            F.MSG: F.UNAVAILABLE,
        }
        super().__init__(*[code, msg, errors], **kwargs)


def Exception404(request, *args, **kwargs):
    payload = {
        F.STATUS: S.HTTP_404_NOT_FOUND,
        F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
        F.CODE: S.HTTP_404_NOT_FOUND.__str__(),
        F.MSG: F.NOT_FOUND,
        F.ERRORS: [],
    }
    response = get_http_response(payload, S.HTTP_404_NOT_FOUND)
    return response


def Exception500(request, *args, **kwargs):
    request_id = request.META["request_id"]
    payload = {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: S.HTTP_500_INTERNAL_SERVER_ERROR.__str__(),
        F.MSG: f"Please contact Administrator with Request ID : {request_id}",
        F.ERRORS: [],
    }
    response = get_http_response(payload, S.HTTP_500_INTERNAL_SERVER_ERROR)
    return response


class UserAlreadyExistsError(UnprocessableError):
    def __init__(self):
        super().__init__(
            errors=[
                {
                    F.FIELD: F.EMAIL,
                    F.CODE: CC.EMAIL_ALREADY_TAKEN,
                    F.KEY: CC.EMAIL_ALREADY_TAKEN,
                    F.MSG: F.EMAIL_ALREADY_TAKEN,
                }
            ]
        )


class InvalidRoleValueError(UnprocessableError):

    def __init__(self, valid_values):
        super().__init__(
            errors=[
                {
                    F.FIELD: F.ROLE,
                    F.CODE: CC.INVALID_ROLE,
                    F.KEY: CC.INVALID_ROLE,
                    F.MSG: F.INVALID_ROLE.format(valid_values),
                }
            ]
        )


class InvalidCredentialsError(UnauthorizedError):
    def __init__(self):
        super().__init__(msg=F.INCORRECT_CREDENTIALS)


class PasswordConflictError(UnprocessableError):

    def __init__(self):
        super().__init__(msg=F.NEW_PASSWORD_CANNOT_BE_SAME_AS_CURRENT_PASSWORD)


class InvalidUIDB64Error(UnprocessableError):
    def __init__(self):
        super().__init__(
            errors=[
                {
                    F.FIELD: F.UIDB64,
                    F.CODE: CC.INVALID_USER,
                    F.KEY: CC.INVALID_USER,
                    F.MESSAGE: F.INVALID_USER,
                }
            ]
        )


class InvalidTokenError(UnprocessableError):
    def __init__(self):
        super().__init__(
            errors=[
                {
                    F.FIELD: F.TOKEN,
                    F.CODE: CC.INVALID_RESET_TOKEN,
                    F.KEY: CC.INVALID_RESET_TOKEN,
                    F.MESSAGE: F.INVALID_RESET_TOKEN,
                }
            ]
        )
