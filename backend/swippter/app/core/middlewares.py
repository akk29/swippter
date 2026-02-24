import json
import uuid
import time
from django.utils.deprecation import MiddlewareMixin
from app.core.exceptions import ExceptionGenerator, UnprocessableError
from app.utils.utilities import F, get_http_response, ENVS
from app.core.logging import Logger
from swippter.settings import DEBUG, ENV

logger = Logger.get_logger()


class JSONValidationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.method in [F.POST, F.PUT, F.PATCH]
            and request.content_type == F.APPLICATION_JSON
        ):
            try:
                json.loads(request.body)
            except json.JSONDecodeError:
                exception = UnprocessableError(errors=[{F.BODY: F.INVALID_JSON}])
                payload = ExceptionGenerator.process_exception(exception)
                response = get_http_response(payload, payload[F.STATUS])
                return response

        return self.get_response(request)


# Add unique Request ID to all the requests
class RequestIDMiddleware(MiddlewareMixin):
    """
    Adds unique request_id to every request and response.
    Automatically included in all logs.
    """

    def process_request(self, request):
        """Generate and attach request_id at start of request"""
        request_id = uuid.uuid4().hex[:12]
        request.request_id = request_id
        request.META[F.REQUEST_ID] = request_id

    def process_response(self, request, response):
        """Add request_id to response headers and body"""
        request_id = getattr(request, F.REQUEST_ID, F.UNKNOWN)
        response[F.X_REQUEST_ID] = request_id
        if hasattr(response, F.CONTENT) and hasattr(response, F.CONTENT_TYPE):
            if response.content and response.content_type == F.APPLICATION_JSON:
                data = json.loads(response.content.decode(F.UTF8))
                data[F.REQUEST_ID] = request_id
                data = {**{F.REQUEST_ID: request_id}, **data}
                response.content = json.dumps(data).encode(F.UTF8)
                response[F.CONTENT_LENGTH] = len(response.content)
        return response


""" To log the information for all type of requests that are hitting the server"""
class LoggingMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        # logger.info("__init__ called") # only once service starts
        super().__init__(get_response)

    def __call__(self, request):
        # logger.info("__call__ called") # called first in middleware
        # response = None
        # if hasattr(self, 'process_request'):
        #     response = self.process_request(request)
        # response = response or self.get_response(request)
        # if hasattr(self, 'process_response'):
        #     response = self.process_response(request, response)
        # return response
        return super().__call__(request)

    def process_request(self, request):
        # logger.info(f"processing request {request}")
        request._start_time = time.time()
        request_id = getattr(request, F.REQUEST_ID, F.UNKNOWN)

        # Base log message
        log_msg = (
            f"[{request_id}] - "
            f"{F.METHOD}: {request.method} - "
            f"{F.PATH}: {request.path} - "
            f"{F.IP}: {self._get_client_ip(request)} - "
            f"{F.USER_AGENT}: {request.META.get(F.HTTP_USER_AGENT, F.UNKNOWN)}"
        )

        # Add query params only in dev/staging
        if DEBUG or ENV in [ENVS.DEV]:
            sanitized_params = request.GET
            if sanitized_params:
                log_msg += f" - {F.QUERY_PARAMS}: {dict(sanitized_params)}"

        logger.info(log_msg)

    def process_response(self, request, response):
        request_id = getattr(request, F.REQUEST_ID, F.UNKNOWN)
        duration = int((time.time() - getattr(request, F.START_TIME, time.time())) * 1000)

        if request.content_type == F.APPLICATION_JSON:
            if hasattr(response, F.EXCEPTION_METADATA):
                meta = response._exception_metadata
                logger.error(
                    f"[{request_id}] --- {duration}ms --- {meta[F.FILE]}:{meta[F.LINE]}:{meta[F.FUNCTION]} - {meta[F.EXCEPTION_REPR]}"
                )
                delattr(response, F.EXCEPTION_METADATA)
            else:
                logger.info(f"[{request_id}] --- {duration}ms") 
        else:
            logger.info(f"[{request_id}] --- {duration}ms")
        return response

    def process_exception(self, request, exception):
        # only called for custom raised exceptions from codebase
        # only if DRF handler is not added in the settings
        # not able to handle library based exceptions
        # hence implemented app.core.exceptions.process_library_exceptions
        # logger.info("processing exception")
        # response = get_http_response({"code": 500})
        return None

    def _get_client_ip(self, request):
        """Extract real client IP (handle proxies)"""
        x_forwarded_for = request.META.get(F.HTTP_X_FORWARDED_FOR)
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get(F.REMOTE_ADDR, F.UNKNOWN)