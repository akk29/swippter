from rest_framework.views import APIView
from app.utils.utilities import F

class BaseAPIView(APIView):
    """
    Base view that adds rate limit headers to all responses
    """
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if hasattr(request, F.THROTTLE_LIMIT):
            response[F.X_RATELIMIT_LIMIT] = str(request.throttle_limit)
            response[F.X_RATELIMIT_REMAINING] = str(request.throttle_remaining)
            response[F.X_RATELIMIT_RESET] = str(request.throttle_reset)

        return response

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if hasattr(self.request, F.THROTTLE_LIMIT):
            response[F.X_RATELIMIT_LIMIT] = str(self.request.throttle_limit)
            response[F.X_RATELIMIT_REMAINING] = str(self.request.throttle_remaining)
            response[F.X_RATELIMIT_RESET] = str(self.request.throttle_reset)

        return response
