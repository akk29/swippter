import bcrypt
import hashlib
import json
import random
import re
from datetime import datetime
from django.http import HttpResponse
from rest_framework import status as S
from swippter.settings import FRONT_URL

"""
CASE CONVENTION FOR FILLER

1. all small or large caps -> invert mapping
    1. first time word usage -> declare all large caps
       word -> "admin" 
       Mapping -> ADMIN = 'admin' # all large

    2. word -> "ADMIN" 
       Mapping -> admin = "ADMIN" # all small

2. for others cases -> exact same mapping
    1. word -> "Admin"
       Mapping -> Admin = "Admin"
    2. word -> "adMIN"
       Mapping -> adMIN = "adMIN"

"""

class ENVS:
    PROD = "prod"
    STAGING = "staging"
    DEV = "dev"

class FILLER:
    # Common or one time / non-context / Single word / Non Space literal / Small    
    ACCESS = "access"
    ADMIN = "admin"
    AFTER = "after"
    ANON = "anon"
    APPLICATION_JSON = "application/json"
    BODY = "body"
    CODE = "code"
    CONNECTED = "connected"
    CONSUMER = "consumer"
    CREATED = "created"
    CONTENT = "content"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_TYPE = "content_type"
    DATA = "data"
    DATABASE = "database"
    DELETED = "deleted"
    DEFAULT = "default"
    ERROR = "error"
    ERRORS = "errors"
    EMAIL = "email"
    EXCEPTION_TYPE = "exception_type"
    EXCEPTION_METADATA = "_exception_metadata"
    EXCEPTION_REPR = "exception_repr"
    FILE = "file"
    FIELD = "field"
    FIRST_NAME = "first_name"   
    FUNCTION = "function" 
    GET_TOKEN = "get_token"
    HEALTHY = "healthy"
    HEALTH_CHECK = "health_check"
    IS_SUPERUSER = "is_superuser"
    IS_STAFF = "is_staff"
    IS_VERIFIED = "is_verified"
    IP = "ip"
    KEY = "key"
    LAST_NAME = "last_name"
    LOC = "loc"
    LINE = "line"
    METHOD = "method"
    MESSAGE = "message"
    MSG = "msg"
    MYSQL = "mysql"
    NAME = "name"
    OK = "ok"
    PATH = "path"
    PASSWORD = "password"    
    PK = "pk"
    QUERY_PARAMS = "query_params"
    RABBITMQ = "rabbitmq"
    RECIEVER = "reciever"
    REFRESH = "refresh"
    REMOTE_ADDR = "REMOTE_ADDR"
    RESET_PASSWORD = "reset_password"
    REQUEST_ID = "request_id"    
    ROLE = "role"
    SALT = "salt"
    SENDER = "sender"
    SELLER = "seller"
    STATUS = "status"
    SUBJECT = "subject"
    SUCCESS = "success"
    SUPER_ADMIN = "super_admin"
    SWIPPTER = "swippter"
    START_TIME = "_start_time"
    THROTTLE_LIMIT = "throttle_limit"
    TOKEN = "token"
    TYPE = "type"
    UNKNOWN = "unknown"
    UNHEALTHY = "unhealthy"
    UIDB64 = "uidb64"
    USER = "user"
    USERNAME = "username"
    USER_AGENT = "user_agent"
    UUID = "uuid"
    UTF8 = "utf-8"
    UPDATED = "updated"
    V1 = "v1"
    VERSION = "version"
    
    # Capital
    A = "A"
    ADMIN_EMAIL = "ADMIN_EMAIL"
    ADMIN_PASSWORD = "ADMIN_PASSWORD"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    OPTIONS = "OPTIONS"
    DELETE = "DELETE"
    Z = "Z"

    # Errors msgs
    BAD_REQUEST = "Bad Request"
    CONFLICT = "Conflict"
    METHOD_NOT_ALLOWED = "Method not allowed"
    FORBIDDEN = "Forbidden"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    NOT_FOUND = "Not found"
    NOT_ACCEPTABLE = "Not Acceptable"
    NOT_IMPLEMENTED = "Not Implemented"
    PARSE_ERROR = "Parse Error"
    TOO_MANY_REQUESTS = "You have made too many requests. Please try again later. Retry after {} seconds"
    UNAUTHORIZED = "Unauthorized"
    UNPROCESSABLE = "Unprocessable"
    UNAVAILABLE = "Unavailable"
    UNSUPPORTED_MEDIA_TYPE = "Unsupported Media Type"

    # Database Error msgs
    DATABASE_INTEGRITY_ERROR = "Data integrity error"
    DATA_INTEGRITY_CONSTRAINT_VOLIATED = "Data integrity constraint violated."
    DATABASE_TEMPORARILY_UNAVAILABLE = "Database temporarily unavailable."
    DATABASE_ERROR_OCCURRED = "Database error occurred."
    DATABASE_DATA_ERROR = "Database data error."
    CANNOT_DELETE_PROTECTED_RESOURCE = "Cannot delete protected resource."
    DATABASE_OPERATION_NOT_SUPPORRTED = "Database operation not supported."
    DATABASE_PROGRAMMING_ERROR = "Database programming error."
    DATABASE_CONNECTION_SUCCESS = "Database is connected."
    DATABASE_CONNECTION_FAILED = "Database is down"
    DATABASE_UNEXPECTED_ERROR = "Database unavailable, An unexpected error occurre while connecting to Database: {}, retrying again ... in {} seconds"

    # Custom Error msgs / business Logic
    EMAIL_MUST_BE_SET = "The given email must be set"
    EMAIL_ALREADY_TAKEN = "The given email is already registered"
    EMAIL_NOT_FOUND = "The given email doesn't exist in our system"
    INCORRECT_CREDENTIALS = "Incorrect credentials"
    INVALID_ROLE = "Role should have these values {}"
    INVALID_USER = "Invalid user"
    INVALID_RESET_TOKEN = "Invalid reset token"
    INVALID_DATA_FORMAT = "Invalid data format."
    INVALID_JSON = "Invalid JSON"
    NEW_PASSWORD_CANNOT_BE_SAME_AS_CURRENT_PASSWORD = (
        "New password can't be same as current password"
    )
    USERNAME_UNAVAILABLE = "Username unavailable"
    USERNAME_NOT_ALLOWED = "Username not allowed"
    USER_NOT_FOUND = "The given user doesn't exist in our system"
    VALIDATION_FAILED = "Validation Failed."
    FIELD_ERROR = "Field Error"
    REQUEST_ABORTED = "Request Aborted"
    EMAIL_IF_USER_EXISTS = (
        "If user exists in our system. You will recieve email shortly."
    )

    CELERY_TASK_PRERUN = "🚀 Task Started: {} [ID: {}]"
    CELERY_TASK_POSTRUN = "✅ Task Completed: {} [ID: {}]"
    CELERY_TASK_FAILURE = "❌ Task Failed: [ID: {}] - {}"
    CELERY_EMAIL_SENDING = "Sending email"
    CELERY_EMAIL_SENT = "Email sent"
    CELERY_EMAIL_SWITCH_OFF = "Sending email is switched off"

    # Logger msgs
    LOGGER_SETUP = "Setting up logger - objID - {}"
    LOGGING_FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(module)s:%(filename)s:%(funcName)s:%(lineno)d --- %(message)s"
    LOGGER_SETUP_SUCCESS = "logger setup complete"

    # Logging Colors
    LOG_GREEN = "\x1b[1;32m"
    LOG_GREY = "\x1b[38;20m"
    LOG_YELLOW = "\x1b[33;20m"
    LOG_RED = "\x1b[31;20m"
    LOG_BOLD_RED = "\x1b[31;1m"
    LOG_RESET = "\x1b[0m"

    # Redis msgs
    REDIS = "redis"
    REDIS_CONNECTION_SUCCESS = "Successfully connected to Redis!"
    REDIS_CANNOT_CONNECTION = "Could not connect to Redis."
    REDIS_KEY = "mykey"
    REDIS_MSG = "hello redis"
    RETRIEVED_VALUE = "Retrieved value:"
    REDIS_CONNECTION_ERROR = "Redis connection error"
    REDIS_UNEXPECTED_ERROR = "Redis unavailable, An unexpected error occurre while connecting to Redis: {}, retrying again ... in {} seconds"
    REDIS_IS_DOWN = "Redis is down"

    RABBITMQ_CONNECTION_SUCCESS = "RabbitMQ broker is available!"
    RABBITMQ_UNEXPECTED_ERROR = "RabbitMQ broker unavailable, An unexpected error occurre while connecting to RabbitMQ: {}, retrying again ... in {} seconds"
    RABBITMQ_IS_DOWN = "RabbitMQ is down"

    # Other strings in Application
    ADMIN_USER_ALREADY_REGISTERED = "Admin user already registered"
    ADMIN_USER_REGISTERED = "Admin user registered"
    ADMIN_USER_NOT_REGISTERED = "Admin user not registered"
    CREATING_ADMIN_USER = "Creating admin user"
    ERROR_IN_ADMIN_EMAIL = "Error in admin email"
    ERROR_IN_ADMIN_PASSWORD = "Error in admin password"

    # simple_jwt related error
    JWT_TOKEN_ERROR = "Token Error"
    JWT_INVALID_TOKEN = "Invalid Token"
    JWT_EXPIRED_TOKEN = "Expired Token"
    JWT_TOKEN_BACKEND_ERROR = "Token Backend Error"
    JWT_TOKEN_BACKEND_EXPIRED_ERROR = "Token Backend Expired Error"
    JWT_AUTHENTICATION_FAILED = "Authentication Failed"

    # Headers
    X_RATELIMIT_LIMIT = "X-RateLimit-Limit"
    X_RATELIMIT_REMAINING = "X-RateLimit-Remaining"
    X_RATELIMIT_RESET = "X-RateLimit-Reset"
    X_REQUEST_ID = "X-Request-Id"
    
    # Http
    HTTP_X_FORWARDED_FOR = "HTTP_X_FORWARDED_FOR"
    HTTP_USER_AGENT = "HTTP_USER_AGENT"
    


F = FILLER


def get_http_response(
    payload={}, status=S.HTTP_200_OK, content_type=F.APPLICATION_JSON
):
    response = HttpResponse(
        json.dumps(payload), status=status, content_type=content_type
    )
    return response


def get_http_response_msg(
    payload={},
    status=S.HTTP_200_OK,
    content_type=F.APPLICATION_JSON,
    message=F.SUCCESS,
):
    response = HttpResponse(
        json.dumps({F.STATUS: status, F.MSG: message, F.DATA: payload}),
        status=status,
        content_type=content_type,
    )
    return response


def my_etag_func(request, **kwargs):
    return hashlib.sha256(f"fixed".encode()).hexdigest()


def my_last_modified_func(request, **kwargs):
    return datetime(2024, 1, 1, 12, 0)


def generate_random_string():
    return "".join([chr(random.randint(ord(F.A), ord(F.Z))) for _ in range(5)])


def generate_salt():
    return bcrypt.gensalt().decode()


def generate_password_hash(password, salt):
    return bcrypt.hashpw(password.encode(F.UTF8), salt.encode(F.UTF8)).decode(F.UTF8)


def is_valid_email(email):
    """Check if the email is a valid format."""
    # Regular expression for validating a standard Email format
    # "name.surname+mail@ireland.gmail-google.uk.com", passing all the cases for email
    regex_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    # Use re.fullmatch() to ensure the entire string matches the pattern
    if re.fullmatch(regex_pattern, email):
        return True
    else:
        return False


def get_item(arr, index):
    try:
        item = arr[index]
        return item
    except IndexError:
        return None

# def generate_token(user):
#     payload = {F.ID : user.id , F.EMAIL  : user.email , F.ROLE : profileTyepMapping[int(user.profiletype)]}
#     return jwt.encode(payload,SECRET_KEY,algorithm=F.HS256).decode(F.UTF8)


def create_reset_message(uidb64, token):
    return f""" Reset password : {FRONT_URL}/verify-token/{uidb64}/{token} """
