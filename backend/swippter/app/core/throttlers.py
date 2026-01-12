from rest_framework.throttling import UserRateThrottle
from app.utils.utilities import F

class CustomRateThrottle(UserRateThrottle):

    scope = F.USER

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

        request.throttle_limit = self.num_requests
        request.throttle_remaining = max(0, self.num_requests - len(self.history))
        request.throttle_reset = int(self.now + self.duration)

        if len(self.history) >= self.num_requests:            
            return self.throttle_failure()
        return self.throttle_success()
    

class CustomAnonRateThrottle(UserRateThrottle):

    scope = F.ANON

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

        request.throttle_limit = self.num_requests
        request.throttle_remaining = max(0, self.num_requests - len(self.history))
        request.throttle_reset = int(self.now + self.duration)

        if len(self.history) >= self.num_requests:            
            return self.throttle_failure()
        return self.throttle_success()