import redis
from rest_framework.throttling import UserRateThrottle
from swippter.settings import REDIS

redis_client = redis.Redis.from_url(REDIS)

class CustomRateThrottle(UserRateThrottle):

    def get_cache_key(self, request, view):
        if request.user:
            # TODO -> After user flow is completed & add this Throttling clas
            # to the global setting of DRF
            # get user info like jwt based authentication & then use that token
            # if not authenticated use header HTTP_X_FORWARDED_FOR to make calculations
            # REMOTE ADDR
            # TRUSTED PROXYS
            # JWT BASED AUTHENTICATION
            # print(self.num_requests-len(self.history))
            pass
        return super().get_cache_key(request, view)

    def allow_request(self, request, view):
        # return self.throttle_failure()
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        redis_client.set(self.key, self.num_requests - len(self.history))
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            redis_client.set(f"{self.key}_retry", int(self.wait()))
            return self.throttle_failure()
        return self.throttle_success()