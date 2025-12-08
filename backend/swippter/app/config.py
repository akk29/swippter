import sys
import redis
from django.apps import AppConfig
from app.core.logging import Logger
from swippter.settings import REDIS
from app.utils.utilities import F

class Starter:

    def __init__(self):
        self.logger = None
        self.redis = None

    def setup_logger(self):
        logger = Logger.setup()
        self.logger = logger
        self.logger.info('logger setup complete')

    def setup_redis(self):
        try:
            r = redis.Redis.from_url(REDIS)
            response = r.ping()
            if response:
                self.logger.info(F.REDIS_CONNECTION_SUCCESS)
            else:
                self.logger.fatal(F.REDIS_CANNOT_CONNECTION)
                sys.exit()
            r.set(F.MY_KEY, F.HELLO_REDIS)
            value = r.get(F.MY_KEY)
            self.logger.info(
                f"{F.RETRIEVED_VALUE} {value.decode(F.UTF8)}"
            )  # Decode bytes to string
        except redis.exceptions.ConnectionError as e:
            self.logger.critical(f"{F.REDIS_CONNECTION_ERROR} {e}")
            sys.exit()
        except Exception as e:
            self.logger.critical(f"{F.UNEXPECTED_ERROR_REDIS} {e}")
            sys.exit()

class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.config"

    def ready(self):
        starter = Starter()
        starter.setup_logger()
        starter.setup_redis()
