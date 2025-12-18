from django.core.exceptions import (
    PermissionDenied,
    FieldError,
    ValidationError,
    BadRequest,
    RequestAborted,
)
from django.urls import Resolver404, NoReverseMatch
from django.http import UnreadablePostError, Http404
from django.db import (
    DatabaseError,
    DataError,
    OperationalError,
    IntegrityError,
    InternalError,
    ProgrammingError,
    NotSupportedError,
)
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status as S
from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler
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
ERROR_MAP = {}

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
    ValidationError: {
        F.STATUS: S.HTTP_422_UNPROCESSABLE_ENTITY,
        F.NAME: ERROR_NAME.UNPROCESSABLE_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST,
        F.MSG: F.DATA_INTEGRITY_CONSTRAINT_VOLIATED,
        F.ERRORS: [],
    },
    BadRequest: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST,
        F.MSG: F.DATA_INTEGRITY_CONSTRAINT_VOLIATED,
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

DB_ERROR_MAP = {
    IntegrityError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST,
        F.MSG: F.DATA_INTEGRITY_CONSTRAINT_VOLIATED,
        F.ERRORS: [],
    },
    # ProtectedError: {
    #     F.STATUS: S.HTTP_409_CONFLICT,
    #     F.NAME: ERROR_NAME.CONFLICT_ERROR,
    #     F.CODE: S.HTTP_409_CONFLICT,
    #     F.MSG: F.CANNOT_DELETE_PROTECTED_RESOURCE,
    #     F.ERRORS: [],
    # },
    # ObjectDoesNotExist: {
    #     F.STATUS: S.HTTP_404_NOT_FOUND,
    #     F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
    #     F.CODE: S.HTTP_404_NOT_FOUND,
    #     F.MSG: F.NOT_FOUND,
    #     F.ERRORS: [],
    # },
    DataError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.BAD_REQUEST_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST,
        F.MSG: F.INVALID_DATA_FORMAT,
        F.ERRORS: [],
    },
    OperationalError: {
        F.STATUS: S.HTTP_503_SERVICE_UNAVAILABLE,
        F.NAME: ERROR_NAME.UNAVAILABLE_ERROR,
        F.CODE: S.HTTP_503_SERVICE_UNAVAILABLE,
        F.MSG: F.DATABASE_TEMPORARILY_UNAVAILABLE,
        F.ERRORS: [],
    },
    DatabaseError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.MSG: F.DATABASE_ERROR_OCCURRED,
        F.ERRORS: [],
    },
    InternalError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    },
    ProgrammingError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.MSG: F.DATABASE_PROGRAMMING_ERROR,
        F.ERRORS: [],
    },
    NotSupportedError: {
        F.STATUS: S.HTTP_501_NOT_IMPLEMENTED,
        F.NAME: ERROR_NAME.NOT_IMPLEMENTED_ERROR,
        F.CODE: S.HTTP_501_NOT_IMPLEMENTED,
        F.MSG: F.DATABASE_OPERATION_NOT_SUPPORRTED,
        F.ERRORS: [],
    },
}

ERROR_MAP.update(DB_ERROR_MAP)


class ExceptionHandler(MiddlewareMixin):

    def process_exception(self, request, exception):
        if isinstance(exception, DatabaseError):
            print(str(exception).lower())
            for exc_type, config in ERROR_MAP.items():
                if isinstance(exception, exc_type):
                    exception = BaseError(
                        *[],
                        **{
                            F.STATUS: config[F.STATUS],
                            F.NAME: config[F.NAME],
                            F.CODE: config[F.CODE],
                            F.MSG: config[F.MSG],
                            F.ERRORS: config[F.ERRORS] or exception.args,
                        },
                    )
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
