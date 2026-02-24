import sys
import redis
import time
from celery import Celery
from django.apps import AppConfig
from django.db import connections
from app.core.logging import Logger
from app.pattern.singleton import SingletonPattern
from app.utils.utilities import F
from kombu.exceptions import OperationalError as KombuError
from swippter.settings import (
    REDIS,
    CELERY_BROKER_URL,
    DB_CRITICAL,
    REDIS_CRITICAL,
    RABBITMQ_CRITICAL,
)


class Starter(SingletonPattern):

    def __init__(self):
        self.logger = Logger.setup()
        self.redis = None

    def setup_logger(self):
        self.logger.info(F.LOGGER_SETUP_SUCCESS)

    def service_checker(
        self,
        check_fxn,
        success_msg,
        exit_msg,
        error_msg,
        max_tries=3,
        attempt=1,
        cap=30,
        critical=True,
    ):
        while True:
            if not max_tries:
                self.logger.critical(exit_msg)
                if critical:
                    sys.exit()
                else:
                    raise
            try:
                check_fxn()
                self.logger.info(success_msg)
                break
            except Exception as e:
                if not critical:  # For first failure if not critical return immediately
                    return None
                delay = min(1 * 2**attempt, cap)
                self.logger.error(error_msg.format(e, delay))
                max_tries -= 1
                attempt += 1
                time.sleep(delay)
        return True

    def setup_redis(self, critical=True):

        def check_redis():
            try:
                r = redis.Redis.from_url(REDIS)
                response = r.ping()
                if response:
                    self.logger.info(F.REDIS_CONNECTION_SUCCESS)
                else:
                    self.logger.fatal(F.REDIS_CANNOT_CONNECTION)
                    sys.exit()
                r.set(F.REDIS_KEY, F.REDIS_MSG)
                value = r.get(F.REDIS_KEY)
                self.logger.info(f"{F.RETRIEVED_VALUE} {value.decode(F.UTF8)}")
                r.close()
            except:
                raise

        self.service_checker(
            check_redis,
            F.REDIS_CONNECTION_SUCCESS,
            F.REDIS_CONNECTION_ERROR,
            F.REDIS_UNEXPECTED_ERROR,
            critical=critical,
        )

    def setup_db(self, critical=True):

        def check_db():
            db_conn = connections[F.DEFAULT]
            try:
                db_conn.cursor()
                db_conn.close()
            except:
                raise

        self.service_checker(
            check_db,
            F.DATABASE_CONNECTION_SUCCESS,
            F.DATABASE_CONNECTION_FAILED,
            F.DATABASE_UNEXPECTED_ERROR,
            critical=critical,
        )

    def setup_rabbitmq(self, critical=True):

        app = Celery(F.SWIPPTER, broker=CELERY_BROKER_URL)

        def check_rabbitmq():
            try:
                app.control.ping()
                app.close()
            except KombuError:
                raise
            except Exception as e:
                raise

        self.service_checker(
            check_rabbitmq,
            F.RABBITMQ_CONNECTION_SUCCESS,
            F.RABBITMQ_IS_DOWN,
            F.RABBITMQ_UNEXPECTED_ERROR,
            critical=critical,
        )


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.config"

    def ready(self):
        starter = Starter()
        starter.setup_logger()
        starter.setup_redis(critical=REDIS_CRITICAL)
        starter.setup_db(critical=DB_CRITICAL)
        starter.setup_rabbitmq(critical=RABBITMQ_CRITICAL)
