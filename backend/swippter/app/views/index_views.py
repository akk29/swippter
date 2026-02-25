from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from app.core.throttlers import CustomRateThrottle
from app.pattern.abstract_factory import DefaultFactory
from app.utils.utilities import (
    F,
    get_http_response_msg,
    my_etag_func,
    my_last_modified_func,
)
from app.config import Starter
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


index_service = DefaultFactory.get_service().index()
starter = Starter.get_instance()


class HealthCheckView(APIView):

    def get(self, request):
        health_status = {
            F.VERSION: F.V1,
            F.METHOD: request.method,
            F.STATUS: F.HEALTHY,
            F.DATABASE: F.UNKNOWN,
            F.REDIS: F.UNKNOWN,
            F.RABBITMQ: F.UNKNOWN,
        }

        try:
            starter.setup_db(critical=False)
            health_status[F.DATABASE] = F.CONNECTED
        except Exception as e:
            health_status[F.DATABASE] = F.UNHEALTHY

        try:
            starter.setup_redis(critical=False)
            health_status[F.REDIS] = F.CONNECTED
        except Exception as e:
            health_status[F.REDIS] = F.UNHEALTHY

        try:
            starter.setup_rabbitmq(critical=False)
            health_status[F.RABBITMQ] = F.CONNECTED
        except Exception as e:
            health_status[F.RABBITMQ] = F.UNHEALTHY

        response = get_http_response_msg(payload=health_status)
        return response


class IndexView(APIView):

    @method_decorator(
        condition(etag_func=my_etag_func, last_modified_func=my_last_modified_func),
        name="dispatch",
    )
    def get(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def post(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def put(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def patch(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def delete(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response

    def options(self, request):
        response = get_http_response_msg({F.VERSION: F.V1, F.METHOD: request.method})
        return response


class RaiseErrorView(APIView):

    throttle_classes = [CustomRateThrottle]

    def post(self, request):
        # raise TokenBackendExpiredToken()
        # raise PermissionDenied()
        # raise DatabaseError()
        # raise DRF_APIException()
        # raise KB_OperationalError()
        # raise REDIS_ConnectionError()
        # raise CL_OperationalError()
        return index_service.raise_error_service()
