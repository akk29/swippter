from django.utils.deprecation import MiddlewareMixin
from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle

#TODO
#Serialize this object and store in redis, After that it will be used in middleware,
#for now revert back the changes related to throttling
# def add_rate_limit_headers(request, response, throttle):
#     """
#     Adds standard rate-limit headers to the response.
#     """
#     response["X-RateLimit-Limit"] = throttle.history or 5
#     response["X-RateLimit-Remaining"] = max(0, throttle.history) or 5
#     # Cooldown only when exhausted
#     retry = throttle.history or 5
#     if retry:
#         response["Retry-After"] = retry
#     return response

def add_rate_limit_headers(request, response, throttle):
    return response

class ThrottleHeaderMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):        
        response = self.get_response(request)
        response = add_rate_limit_headers(request, response,None)
        return response


class CustomRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()