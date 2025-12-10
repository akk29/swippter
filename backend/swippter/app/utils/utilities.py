import json
import bcrypt
import hashlib
import random
from datetime import datetime
from django.http import HttpResponse
from rest_framework import status as S

class FILLER:
    # Common or one time / non-context
    A = "A"
    ADMIN = "admin"
    APPLICATION_JSON = "application/json"
    CODE = "code"
    ERRORS = "errors"
    EMAIL = "email"
    FIELD = "field"
    FIRST_NAME = "first_name"
    IS_SUPERUSER = "is_superuser"
    IS_STAFF = "is_staff"
    IS_VERIFIED = "is_verified"
    KEY = "key"
    LAST_NAME = 'last_name'
    METHOD = "method"
    MESSAGE = "message"
    MSG = "msg"
    MYSQL = "mysql"
    NAME = "name"
    RECIEVER = "reciever"
    ROLE = "role"
    SALT = 'salt'
    SENDER = "sender"
    STATUS = "status"
    SUBJECT = "subject"
    USERNAME = "username"
    VERSION = "version"
    V1 = "v1"
    UTF8 = "utf-8"
    Z = "Z"

    # Colors
    GREEN = "\x1b[1;32m"
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    # Errors msgs
    BAD_REQUEST = "Bad Request"
    METHOD_NOT_ALLOWED = "Method not allowed"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    NOT_FOUND = "Not found"
    FORBIDDEN = "Forbidden"
    UNAUTHORIZED = "Unauthorized"
    TOO_MANY_REQUESTS = "You have made too many requests. Please try again later. Retry after {} seconds"
    UNPROCESSABLE = "Unprocessable"

    # Custom Error msgs / Business Logic
    USERNAME_UNAVAILABLE = "Username unavailable"
    USERNAME_NOT_ALLOWED = "Username not allowed"
    EMAIL_MUST_BE_SET = "The given email must be set"

    # Logger msgs
    LOGGER_SETUP = "Setting up logger - objID - {}"
    LOGGING_FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(module)s:%(filename)s:%(funcName)s:%(lineno)d --- %(message)s"

    # Redis msgs
    REDIS_CONNECTION_SUCCESS = "Successfully connected to Redis!"
    REDIS_CANNOT_CONNECTION = "Could not connect to Redis."
    MY_KEY = "mykey"
    HELLO_REDIS = "hello redis"
    RETRIEVED_VALUE = "Retrieved value:"
    REDIS_CONNECTION_ERROR = "Redis connection error:"
    UNEXPECTED_ERROR_REDIS = "An unexpected error occurred:"


F = FILLER

def get_http_response(
    payload=None, status=S.HTTP_200_OK, content_type=F.APPLICATION_JSON
):
    response = HttpResponse(
        json.dumps(payload), status=status, content_type=F.APPLICATION_JSON
    )
    return response

def my_etag_func(request, **kwargs):
    return hashlib.sha256(f"fixed".encode()).hexdigest()

def my_last_modified_func(request, **kwargs):
    return datetime(2024, 1, 1, 12, 0)

def generate_random_string():
    return "".join([chr(random.randint(ord(F.A), ord(F.Z))) for _ in range(5)])

def generate_salt():
    return bcrypt.gensalt()

def generate_password_hash(password,salt):    
    return bcrypt.hashpw(password.encode(F.UTF8), salt)