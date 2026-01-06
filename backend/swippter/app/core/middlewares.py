import redis
import json
from django.utils.deprecation import MiddlewareMixin
from app.core.exceptions import ExceptionGenerator, UnprocessableError
from app.models.user import Role
from app.utils.utilities import F, get_http_response
from swippter.settings import REDIS, THROTTLE_RATE

redis_client = redis.Redis.from_url(REDIS)

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


class ThrottleHeaderMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response = self.add_rate_limit_headers(request, response, None)
        return response

    def add_rate_limit_headers(self, request, response, throttle):
        # TODO
        if not request.user.is_anonymous:
            if request.user.role == Role.SUPER_ADMIN:
                return response
        remaining_limit = int(
            redis_client.get(f"throttle_user_{request.META['REMOTE_ADDR']}") or 0
        )
        response["X-RateLimit-Limit"] = THROTTLE_RATE.split("/")[0]
        if remaining_limit > 0:
            response["X-RateLimit-Remaining"] = remaining_limit
            return response
        else:
            retry_after = int(
                redis_client.get(f"throttle_user_{request.META['REMOTE_ADDR']}_retry")
                or 0
            )
            response["Retry-After"] = retry_after
            return response
