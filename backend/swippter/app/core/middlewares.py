import json
from django.utils.deprecation import MiddlewareMixin
from app.core.exceptions import ExceptionGenerator, UnprocessableError
from app.utils.utilities import F, get_http_response

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
