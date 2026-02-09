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
from kombu.exceptions import (
    OperationalError as KB_OperationalError,  # Broker unreachable
    ConnectionError as KB_ConnectionError,  # Connection dropped
    TimeoutError as KB_TimeoutError,  # Operation timed out
    KombuError as KB_KombuError,  # Base class (catch-all)
)
from amqp.exceptions import (
    ConnectionError,  # Low-level connection failure
    ChannelError,  # Channel-level error
    AccessRefused,  # Auth failed
    NotFound,  # Queue/exchange missing
    PreconditionFailed,  # Queue config mismatch
)
from redis.exceptions import (
    ConnectionError as REDIS_ConnectionError,  # Can't connect to Redis
    TimeoutError,  # Connection/operation timed out
    AuthenticationError,  # Wrong password
    ResponseError,  # Wrong command for data type
    DataError,  # Invalid data for operation
    RedisError,  # Base class (catch-all)
)
from celery.exceptions import (
    OperationalError as CL_OperationalError,  # Worker/broker operational failure
    TimeoutError as CL_TimeoutError,  # Task execution timed out
    TaskRevokedError as CL_TaskRevokedError,  # Task was manually revoked
    WorkerLostError as CL_WorkerLostError,  # Worker died during task
    Retry as CL_Retry,  # Task is being retried (not an error)
    MaxRetriesExceededError as CL_MaxRetriesExceededError,  # Hit retry limit
    NotRegistered as CL_NotRegistered,  # Task not found in registry
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

# CUSTOM CODE -> INHERIT FROM SUFFIX OF UUIDV4
# GENERATE THESE CODE FROM SUBSTRING OF UUID TO KEEP IT RANDOM AND SCALABLE
# SUPPORTING LEGACY SOFTWARE AND FUTURE DEVELOPMENT SCOPE
class APPLICATION_ERRORS:
    # E
    EMAIL_MUST_BE_SET = "a1b2c3d4"
    EMAIL_ALREADY_TAKEN = "b2c3d4e5"
    EMAIL_NOT_FOUND = "c3d4e5f6"

    # I
    INVALID_ROLE = "d4e5f6a7"
    INVALID_USER = "e5f6a7b8"
    INVALID_RESET_TOKEN = "f6a7b8c9"
    INVAID_CREDENTIALS = "a7b8c9d0"


class DATABASE_ERRORS:
    DATABASE_TEMPORARILY_UNAVAILABLE = "b7c8d9e0"
    DATABASE_DATA_ERROR = "c8d9e0f1"
    DATABASE_INTEGRITY_ERROR = "d9e0f1a2"
    DATABASE_OPERATION_NOT_SUPPORRTED = "e0f1a2b3"
    DATABASE_INTERNAL_ERROR = "f1a2b3c4"
    DATABASE_ERROR = "a2b3c4d5"
    DATABASE_PROGRAMMING_ERROR = "b3c4d5e6"


class DRF_ERRORS:
    DRF_API_EXCEPTION = "c4d5e6f7"
    DRF_VALIDATION_EXCEPTION = "d5e6f7a8"
    DRF_PARSE_ERROR = "e6f7a8b9"
    DRF_AUTHENTICATION_FAILED = "f7a8b9c0"
    DRF_NOT_AUTHENTICATED = "a8b9c0d1"
    DRF_PERMISSION_DENIED = "b9c0d1e2"
    DRF_NOT_FOUND = "c0d1e2f3"
    DRF_METHOD_NOT_ALLOWED = "d1e2f3a4"
    DRF_NOT_ACCEPTABLE = "e2f3a4b5"
    DRF_UNSUPPORTED_MEDIA_TYPE = "f3a4b5c6"
    DRF_THROTTLED = "a4b5c6d7"


class JWT_ERRORS:
    JWT_TOKEN_ERROR = "b4c5d6e7"
    JWT_EXPIRED_TOKEN_ERROR = "c5d6e7f8"
    JWT_INVALID_TOKEN = "d6e7f8a9"
    JWT_TOKEN_BACKEND_ERROR = "e7f8a9b0"
    JWT_TOKEN_BACKEND_EXPIRED_TOKEN = "f8a9b0c1"
    JWT_AUTHENTICATION_FAILED = "a9b0c1d2"

class REDIS_ERRORS:
    REDIS_CONNECTION_ERROR = "b0c1d2e3"

class PYDANTIC_ERRORS:
    PYDANTIC_VALIDATION = "c1d2e3f4"

class CELERY_ERRORS:
    CELERY_OPERATIONAL_ERROR = "d2e3f4a5"

class RABBITMQ_ERRORS:
    RABBITMQ_CONNECTION_ERROR = "e3f4a5b6"

class CUSTOM_CODE(
    APPLICATION_ERRORS,
    DATABASE_ERRORS,
    DRF_ERRORS,
    JWT_ERRORS,
    REDIS_ERRORS,
    PYDANTIC_ERRORS,
    CELERY_ERRORS,
    RABBITMQ_ERRORS
):
    pass


# ============================================
# Django Framework Errors
# ============================================

EXCEPTION_ERROR_MAP = {
    PermissionDenied: {
        F.STATUS: S.HTTP_403_FORBIDDEN,
        F.NAME: ERROR_NAME.FORBIDDEN_ERROR,
        F.CODE: S.HTTP_403_FORBIDDEN.__str__(),
        F.MSG: F.FORBIDDEN,
        F.ERRORS: [],
    },
    FieldError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST.__str__(),
        F.MSG: F.FIELD_ERROR,
        F.ERRORS: [],
    },
    ObjectDoesNotExist: {
        F.STATUS: S.HTTP_404_NOT_FOUND,
        F.NAME: ERROR_NAME.NOT_FOUND_ERROR,
        F.CODE: S.HTTP_404_NOT_FOUND.__str__(),
        F.MSG: F.NOT_FOUND,
        F.ERRORS: [],
    },
    ValidationError: {
        F.STATUS: S.HTTP_422_UNPROCESSABLE_ENTITY,
        F.NAME: ERROR_NAME.UNPROCESSABLE_ERROR,
        F.CODE: S.HTTP_422_UNPROCESSABLE_ENTITY.__str__(),
        F.MSG: F.UNPROCESSABLE,
        F.ERRORS: [],
    },
    BadRequest: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST.__str__(),
        F.MSG: F.BAD_REQUEST,
        F.ERRORS: [],
    },
    RequestAborted: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.INTEGRITY_ERROR,
        F.CODE: S.HTTP_400_BAD_REQUEST.__str__(),
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
    #     F.CODE: S.HTTP_409_CONFLICT.__str__(),
    #     F.MSG: F.CANNOT_DELETE_PROTECTED_RESOURCE,
    #     F.ERRORS: [],
    # },
    DataError: {
        F.STATUS: S.HTTP_400_BAD_REQUEST,
        F.NAME: ERROR_NAME.BAD_REQUEST_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_DATA_ERROR,
        F.MSG: F.BAD_REQUEST,
        F.ERRORS: [],
    },
    # DROP Database
    OperationalError: {
        F.STATUS: S.HTTP_503_SERVICE_UNAVAILABLE,
        F.NAME: ERROR_NAME.UNAVAILABLE_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_TEMPORARILY_UNAVAILABLE,
        F.MSG: F.UNAVAILABLE,
        F.ERRORS: [],
    },
    # Voilate constraint
    DatabaseError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_ERROR,
        F.MSG: F.INTERNAL_SERVER_ERROR,
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
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    },
    NotSupportedError: {
        F.STATUS: S.HTTP_501_NOT_IMPLEMENTED,
        F.NAME: ERROR_NAME.NOT_IMPLEMENTED_ERROR,
        F.CODE: CUSTOM_CODE.DATABASE_OPERATION_NOT_SUPPORRTED,
        F.MSG: F.NOT_IMPLEMENTED,
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
        F.MSG: F.BAD_REQUEST,
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


REDIS_ERROR_MAP = {
    REDIS_ConnectionError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.REDIS_CONNECTION_ERROR,
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    }
}

CELERY_ERROR_MAP = {
    CL_OperationalError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.CELERY_OPERATIONAL_ERROR,
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    }
}

RABBITMQ_ERROR_MAP = {
    KB_OperationalError: {
        F.STATUS: S.HTTP_500_INTERNAL_SERVER_ERROR,
        F.NAME: ERROR_NAME.INTERNAL_SERVER_ERROR,
        F.CODE: CUSTOM_CODE.RABBITMQ_CONNECTION_ERROR,
        F.MSG: F.INTERNAL_SERVER_ERROR,
        F.ERRORS: [],
    }
}