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
from rest_framework.exceptions import (
    APIException as DRF_APIException,
    ValidationError as DRF_ValidationError,
    ParseError as DRF_ParseError,
    AuthenticationFailed as DRF_AuthenticationFailed,
    NotAuthenticated as DRF_NotAuthenticated,
    PermissionDenied as DRF_PermissionDenied,
    NotFound as DRF_NotFound,
    MethodNotAllowed as DRF_MethodNotAllowed,
    NotAcceptable as DRF_NotAcceptable,
    UnsupportedMediaType as DRF_UnsupportedMediaType,
)
from rest_framework_simplejwt.exceptions import (
    TokenError,
    ExpiredTokenError,
    InvalidToken,
    TokenBackendError,
    TokenBackendExpiredToken,
    AuthenticationFailed,
)
from app.utils.utilities import F

class ERROR_NAME:
    BAD_REQUEST_ERROR = "BAD_REQUEST_ERROR"
    CONFLICT_ERROR = "CONFLICT_ERROR"
    FORBIDDEN_ERROR = "FORBIDDEN_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    INTEGRITY_ERROR = "INTEGRITY_ERROR"
    METHOD_NOT_ALLOWED_ERROR = "METHOD_NOT_ALLOWED_ERROR"
    NOT_ACCEPTABLE = "NOT_ACCEPTABLE"
    NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
    NOT_IMPLEMENTED_ERROR = "NOT_IMPLEMENTED_ERROR"
    TOO_MANY_REQUESTS_ERROR = "TOO_MANY_REQUESTS_ERROR"
    UNAUTHORIZED_ERROR = "UNAUTHORIZED_ERROR"
    UNAVAILABLE_ERROR = "UNAVAILABLE_ERROR"
    UNPROCESSABLE_ERROR = "UNPROCESSABLE_ERROR"
    UNSUPPORTED_MEDIA_TYPE = "UNSUPPORTED_MEDIA_TYPE"


class APPLICATION_ERRORS:
    # E
    EMAIL_MUST_BE_SET = "2886623e"
    EMAIL_ALREADY_TAKEN = "28855239"
    EMAIL_NOT_FOUND = "28855239"

    # I
    INVALID_ROLE = "83905850"
    INVALID_USER = "83905851"
    INVALID_RESET_TOKEN = "83905852"


class DATABASE_ERRORS:
    DATABASE_TEMPORARILY_UNAVAILABLE = "23905853"
    DATABASE_DATA_ERROR = "23905863"
    DATABASE_INTEGRITY_ERROR = "23905873"
    DATABASE_OPERATION_NOT_SUPPORRTED = "23905893"
    DATABASE_INTERNAL_ERROR = "23905894"
    DATABASE_ERROR = "23905895"
    DATABASE_PROGRAMMING_ERROR = "23905896"


class DRF_ERRORS:
    DRF_API_EXCEPTION = "24905853"
    DRF_VALIDATION_EXCEPTION = "24905854"
    DRF_PARSE_ERROR = "24905855"
    DRF_AUTHENTICATION_FAILED = "24905856"
    DRF_NOT_AUTHENTICATED = "24905857"
    DRF_PERMISSION_DENIED = "24905858"
    DRF_NOT_FOUND = "24905859"
    DRF_METHOD_NOT_ALLOWED = "24905860"
    DRF_NOT_ACCEPTABLE = "24905861"
    DRF_UNSUPPORTED_MEDIA_TYPE = "24905862"
    DRF_THROTTLED = "24905863"


class JWT_ERRORS:
    JWT_TOKEN_ERROR = "24505861"
    JWT_EXPIRED_TOKEN_ERROR = "24505862"
    JWT_INVALID_TOKEN = "24505863"
    JWT_TOKEN_BACKEND_ERROR = "24505864"
    JWT_TOKEN_BACKEND_EXPIRED_TOKEN = "24505865"
    JWT_AUTHENTICATION_FAILED = "24505866"


class PYDANTIC_ERRORS:
    # P
    PYDANTIC_VALIDATION = "37023855"

# CUSTOM CODE
class CUSTOM_CODE(
    APPLICATION_ERRORS, DATABASE_ERRORS, DRF_ERRORS, JWT_ERRORS, PYDANTIC_ERRORS
):
    pass

# ============================================
# Django Framework Errors
# ============================================

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
        F.MSG: F.FIELD_ERROR,
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
        F.MSG: F.REQUEST_ABORTED,
        F.ERRORS: [],
    },
}

JWT_ERRORS_MAP = {
    TokenError: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.JWT_TOKEN_ERROR,
        F.MSG: F.JWT_TOKEN_ERROR,
        F.ERRORS: [],
    },
    ExpiredTokenError: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.JWT_EXPIRED_TOKEN_ERROR,
        F.MSG: F.JWT_EXPIRED_TOKEN,
        F.ERRORS: [],
    },
    InvalidToken: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.JWT_INVALID_TOKEN,
        F.MSG: F.JWT_INVALID_TOKEN,
        F.ERRORS: [],
    },
    TokenBackendError: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.JWT_TOKEN_BACKEND_ERROR,
        F.MSG: F.JWT_TOKEN_BACKEND_ERROR,
        F.ERRORS: [],
    },
    TokenBackendExpiredToken: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.JWT_TOKEN_BACKEND_EXPIRED_TOKEN,
        F.MSG: F.JWT_TOKEN_BACKEND_EXPIRED_ERROR,
        F.ERRORS: [],
    },
    AuthenticationFailed: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.JWT_AUTHENTICATION_FAILED,
        F.MSG: F.JWT_AUTHENTICATION_FAILED,
        F.ERRORS: [],
    },
}

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

""" DJANGO REST FRAMEWORK MAPPING"""
DRF_EXCEPTION_MAP = {
    DRF_APIException: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.DRF_API_EXCEPTION,
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    },
    DRF_ValidationError: {
        F.STATUS: S.HTTP_422_UNPROCESSABLE_ENTITY,
        F.NAME: ERROR_NAME.UNPROCESSABLE_ERROR,
        F.CODE: CUSTOM_CODE.DRF_VALIDATION_EXCEPTION,
        F.MSG: F.UNPROCESSABLE,
        F.ERRORS: [],
    },
    DRF_ParseError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.BAD_REQUEST_ERROR,
        F.CODE: CUSTOM_CODE.DRF_PARSE_ERROR,
        F.MSG: F.PARSE_ERROR,
        F.ERRORS: [],
    },
    DRF_AuthenticationFailed: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.DRF_AUTHENTICATION_FAILED,
        F.MSG: F.UNAUTHORIZED,
        F.ERRORS: [],
    },
    DRF_PermissionDenied: {
        F.STATUS: S.HTTP_403_FORBIDDEN,
        F.NAME: ERROR_NAME.FORBIDDEN_ERROR,
        F.CODE: CUSTOM_CODE.DRF_PERMISSION_DENIED,
        F.MSG: F.FORBIDDEN,
        F.ERRORS: [],
    },
    DRF_NotFound: {
        F.STATUS: S.HTTP_404_NOT_FOUND,
        F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
        F.CODE: CUSTOM_CODE.DRF_NOT_FOUND,
        F.MSG: F.NOT_FOUND,
        F.ERRORS: [],
    },
    DRF_NotAuthenticated: {
        F.STATUS: S.HTTP_401_UNAUTHORIZED,
        F.NAME: ERROR_NAME.UNAUTHORIZED_ERROR,
        F.CODE: CUSTOM_CODE.DRF_NOT_AUTHENTICATED,
        F.MSG: F.UNAUTHORIZED,
        F.ERRORS: [],
    },
    DRF_MethodNotAllowed: {
        F.STATUS: S.HTTP_405_METHOD_NOT_ALLOWED,
        F.NAME: ERROR_NAME.METHOD_NOT_ALLOWED_ERROR,
        F.CODE: CUSTOM_CODE.DRF_METHOD_NOT_ALLOWED,
        F.MSG: F.METHOD_NOT_ALLOWED,
        F.ERRORS: [],
    },
    DRF_NotAcceptable: {
        F.STATUS: S.HTTP_406_NOT_ACCEPTABLE,
        F.NAME: ERROR_NAME.NOT_ACCEPTABLE,
        F.CODE: CUSTOM_CODE.DRF_NOT_ACCEPTABLE,
        F.MSG: F.NOT_ACCEPTABLE,
        F.ERRORS: [],
    },
    DRF_UnsupportedMediaType: {
        F.STATUS: S.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        F.NAME: ERROR_NAME.UNSUPPORTED_MEDIA_TYPE,
        F.CODE: CUSTOM_CODE.DRF_UNSUPPORTED_MEDIA_TYPE,
        F.MSG: F.UNSUPPORTED_MEDIA_TYPE,
        F.ERRORS: [],
    },
}
