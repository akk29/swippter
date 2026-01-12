from django.core.exceptions import (
    PermissionDenied,
    FieldError,
    ValidationError,
    BadRequest,
    RequestAborted,
    ObjectDoesNotExist,
)
from django.db import (
    DatabaseError,
    DataError,
    OperationalError,
    IntegrityError,  # ProtectedError and RestrictedError
    InternalError,
    ProgrammingError,
    NotSupportedError,
)
from django.http import UnreadablePostError, Http404
from django.urls import Resolver404, NoReverseMatch
from rest_framework import status as S
from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import (
    TokenError,
    ExpiredTokenError,
    InvalidToken,
    TokenBackendError,
    TokenBackendExpiredToken,
    AuthenticationFailed,
)
from app.core.logging import Logger
from app.utils.utilities import F, get_http_response, generate_random_string, get_item

logger = Logger.get_logger()


class ERROR_NAME:
    BAD_REQUEST_ERROR = "BAD_REQUEST_ERROR"
    CONFLICT_ERROR = "CONFLICT_ERROR"
    FORBIDDEN_ERROR = "FORBIDDEN_ERROR"
    METHOD_NOT_ALLOWED_ERROR = "METHOD_NOT_ALLOWED_ERROR"
    NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
    UNAUTHORIZED_ERROR = "UNAUTHORIZED_ERROR"
    UNPROCESSABLE_ERROR = "UNPROCESSABLE_ERROR"
    TOO_MANY_REQUESTS_ERROR = "TOO_MANY_REQUESTS_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNAVAILABLE_ERROR = "UNAVAILABLE_ERROR"
    NOT_IMPLEMENTED_ERROR = "NOT_IMPLEMENTED_ERROR"
    INTEGRITY_ERROR = "INTEGRITY_ERROR"


# Application / Business Logic Based Errors
class CUSTOM_CODE:
    
    #D
    DATABASE_TEMPORARILY_UNAVAILABLE = "23905853"
    DATABASE_DATA_ERROR = "23905863"
    DATABASE_INTEGRITY_ERROR = "23905873"
    DATABASE_OPERATION_NOT_SUPPORRTED = "23905893"
    DATABASE_INTERNAL_ERROR = "23905894"
    DATABASE_ERROR = "23905895"
    DATABASE_PROGRAMMING_ERROR = "23905896"

    #E
    EMAIL_MUST_BE_SET = "2886623e"
    EMAIL_ALREADY_TAKEN = "28855239"
    EMAIL_NOT_FOUND = "28855239"
    
    #P
    PYDANTIC_VALIDATION = "37023855"
    
    #I
    INVALID_ROLE = "83905850"
    INVALID_USER = "83905851"
    INVALID_RESET_TOKEN = "83905852"

    

    @classmethod
    def get(cls, value):
        """Get variable name by its value"""
        for name, val in vars(cls).items():
            if not name.startswith("_") and not callable(val) and val == value:
                return name
        return None


def process_library_exceptions(exc, context):
    response = exception_handler(exc, context)
    # request = context.get('request')

    ''' rest_framework_simplejwt related error interception '''
    if any([True for _ in JWT_ERRORS_MAP.keys() if type(exc) == _]):
        payload = JWT_ERRORS_MAP[type(exc)]
        response = Response(payload,status=payload[F.STATUS])
        return response
    
    ''' django-rest-framework error interception '''
    if response is not None and response.status_code == S.HTTP_401_UNAUTHORIZED:
        payload = {
            F.STATUS: S.HTTP_401_UNAUTHORIZED,
            F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
            F.CODE: S.HTTP_401_UNAUTHORIZED,
            F.MSG: F.UNAUTHORIZED,
            F.ERRORS: [],
        }
        response.data = payload
        return response

    if response is not None and response.status_code == S.HTTP_405_METHOD_NOT_ALLOWED:
        payload = {
            F.STATUS: S.HTTP_405_METHOD_NOT_ALLOWED,
            F.NAME: ERROR_NAME.METHOD_NOT_ALLOWED_ERROR,
            F.CODE: S.HTTP_405_METHOD_NOT_ALLOWED,
            F.MSG: F.METHOD_NOT_ALLOWED,
            F.ERRORS: [],
        }
        response.data = payload
        return response
    
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

    if isinstance(exc, DatabaseError):
        for exc_type, config in DB_ERROR_MAP.items():
            if isinstance(exc, exc_type):
                exc = BaseError(
                    *[],
                    **{
                        F.STATUS: config[F.STATUS],
                        F.NAME: config[F.NAME],
                        F.CODE: config[F.CODE],
                        F.MSG: config[F.MSG],
                        F.ERRORS: config[F.ERRORS] or exc.args,
                    },
                )

    ''' Django internal error interception'''
    if any([True for _ in EXCEPTION_ERROR_MAP.keys() if type(exc) == _]):
        payload = EXCEPTION_ERROR_MAP[type(exc)]
        response.data = payload
        return response
    
    payload = ExceptionGenerator.process_exception(exc)
    response = get_http_response(payload, payload[F.STATUS])
    return response

# ============================================
# Django Framework Errors
# ============================================
"""
Django Database Exception Hierarchy:
- DatabaseError (base class)
  ├── DataError (data processing errors)
  ├── OperationalError (database operational errors)
  ├── IntegrityError (constraint violations) # Unique, Foreign Key, Not Null
  ├── InternalError (internal database errors)
  ├── ProgrammingError (SQL programming errors)
  └── NotSupportedError (unsupported operations)
"""

EXCEPTION_ERROR_MAP = {
    PermissionDenied: {
        F.STATUS: S.HTTP_403_FORBIDDEN,
        F.NAME: ERROR_NAME.FORBIDDEN_ERROR,
        F.CODE: S.HTTP_403_FORBIDDEN,
        F.MSG: F.FORBIDDEN,
        F.ERRORS: [],
    },
    FieldError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST,
        F.MSG: F.DATA_INTEGRITY_CONSTRAINT_VOLIATED,
        F.ERRORS: [],
    },
    ObjectDoesNotExist: {
        F.STATUS: S.HTTP_404_NOT_FOUND,
        F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
        F.CODE: S.HTTP_404_NOT_FOUND,
        F.MSG: F.NOT_FOUND,
        F.ERRORS: [],
    },
    ValidationError: {
        F.STATUS: S.HTTP_422_UNPROCESSABLE_ENTITY,
        F.NAME: ERROR_NAME.UNPROCESSABLE_ERROR,
        F.CODE: S.HTTP_422_UNPROCESSABLE_ENTITY,
        F.MSG: F.UNPROCESSABLE,
        F.ERRORS: [],
    },
    BadRequest: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST,
        F.MSG: F.BAD_REQUEST,
        F.ERRORS: [],
    },
    RequestAborted: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST,
        F.MSG: F.DATA_INTEGRITY_CONSTRAINT_VOLIATED,
        F.ERRORS: [],
    },
}

JWT_ERRORS_MAP = {
    TokenError: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: S.HTTP_401_UNAUTHORIZED,
        F.MSG: F.TOKEN_ERROR,
        F.ERRORS: [],
    },
    ExpiredTokenError: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: S.HTTP_401_UNAUTHORIZED,
        F.MSG: F.EXPIRED_TOKEN,
        F.ERRORS: [],
    },
    InvalidToken: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: S.HTTP_401_UNAUTHORIZED,
        F.MSG: F.INVALID_TOKEN,
        F.ERRORS: [],
    },
    TokenBackendError: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: S.HTTP_401_UNAUTHORIZED,
        F.MSG: F.TOKEN_BACKEND_ERROR,
        F.ERRORS: [],
    },
    TokenBackendExpiredToken: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: S.HTTP_401_UNAUTHORIZED,
        F.MSG: F.TOKEN_BACKEND_EXPIRED_ERROR,
        F.ERRORS: [],
    },
    AuthenticationFailed: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: S.HTTP_401_UNAUTHORIZED,
        F.MSG: F.AUTHENTICATION_FAILED,
        F.ERRORS: [],
    },
}

DB_ERROR_MAP = {
    IntegrityError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.BAD_REQUEST_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_INTEGRITY_ERROR,
        F.MSG: F.DATABASE_INTEGRITY_ERROR,
        F.ERRORS: [],
    },
    # ProtectedError: {
    #     F.STATUS: S.HTTP_409_CONFLICT,
    #     F.NAME: ERROR_NAME.CONFLICT_ERROR,
    #     F.CODE: S.HTTP_409_CONFLICT,
    #     F.MSG: F.CANNOT_DELETE_PROTECTED_RESOURCE,
    #     F.ERRORS: [],
    # },
    DataError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.BAD_REQUEST_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_DATA_ERROR,
        F.MSG: F.DATABASE_DATA_ERROR,
        F.ERRORS: [],
    },
    # DROP Database
    OperationalError: {
        F.STATUS: S.HTTP_503_SERVICE_UNAVAILABLE,
        F.NAME: ERROR_NAME.UNAVAILABLE_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_TEMPORARILY_UNAVAILABLE,
        F.MSG: F.DATABASE_TEMPORARILY_UNAVAILABLE,
        F.ERRORS: [],
    },
    # Voilate constraint
    DatabaseError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_ERROR,
        F.MSG: F.DATABASE_ERROR_OCCURRED,
        F.ERRORS: [],
    },
    InternalError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_INTERNAL_ERROR,
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    },
    ProgrammingError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_PROGRAMMING_ERROR,
        F.MSG: F.DATABASE_PROGRAMMING_ERROR,
        F.ERRORS: [],
    },
    NotSupportedError: {
        F.STATUS: S.HTTP_501_NOT_IMPLEMENTED,
        F.NAME: ERROR_NAME.NOT_IMPLEMENTED_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_OPERATION_NOT_SUPPORRTED,
        F.MSG: F.DATABASE_OPERATION_NOT_SUPPORRTED,
        F.ERRORS: [],
    },
}


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


# ============================================
# COMMON MYSQL ERROR CODES
# ============================================

"""
{'status': 400, 'name': 'INTEGRITY_ERROR', 'code': 400, 'msg': 'Data integrity constraint violated.', 'errors': (1062, "Duplicate entry 'hhc2@c.com' for key 'app_user.email'")}
"""

"""
MySQL Error Codes Reference:
- 1062: ER_DUP_ENTRY - Duplicate entry for key
- 1452: ER_NO_REFERENCED_ROW_2 - Foreign key constraint fails (child row)
- 1451: ER_ROW_IS_REFERENCED_2 - Cannot delete/update parent row (FK constraint)
- 1048: ER_BAD_NULL_ERROR - Column cannot be null
- 1406: ER_DATA_TOO_LONG - Data too long for column
- 1264: ER_WARN_DATA_OUT_OF_RANGE - Out of range value
- 1690: ER_WARN_DATA_OUT_OF_RANGE - BIGINT UNSIGNED value out of range
- 1054: ER_BAD_FIELD_ERROR - Unknown column
- 1146: ER_NO_SUCH_TABLE - Table doesn't exist
- 2003: CR_CONNECTION_ERROR - Can't connect to MySQL server
- 2006: CR_SERVER_GONE_ERROR - MySQL server has gone away
- 2013: CR_SERVER_LOST - Lost connection to MySQL server during query
- 1205: ER_LOCK_WAIT_TIMEOUT - Lock wait timeout exceeded
- 1213: ER_LOCK_DEADLOCK - Deadlock found when trying to get lock
"""
