import json
import bcrypt
import hashlib
import random
import re
from datetime import datetime
from django.http import HttpResponse
from rest_framework import status as S

'''
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

'''

class FILLER:
    # Common or one time / non-context / Single word / Non Space literal
    A = "A"
    ADMIN = "admin"
    ADMIN_EMAIL = "ADMIN_EMAIL"
    ADMIN_PASSWORD = "ADMIN_PASSWORD"
    APPLICATION_JSON = "application/json"
    BODY = "body"
    CODE = "code"
    CONSUMER = "consumer"
    ERRORS = "errors"
    EMAIL = "email"
    FIELD = "field"
    FIRST_NAME = "first_name"
    IS_SUPERUSER = "is_superuser"
    IS_STAFF = "is_staff"
    IS_VERIFIED = "is_verified"
    KEY = "key"
    LAST_NAME = "last_name"
    METHOD = "method"
    MESSAGE = "message"
    MSG = "msg"
    MYSQL = "mysql"
    NAME = "name"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    RECIEVER = "reciever"
    ROLE = "role"
    SALT = "salt"
    SENDER = "sender"
    SELLER = "seller"
    STATUS = "status"
    SUBJECT = "subject"
    SUPER_ADMIN = "super_admin"
    USERNAME = "username"
    VERSION = "version"
    V1 = "v1"
    UTF8 = "utf-8"
    Z = "Z"

    # Errors msgs
    BAD_REQUEST = "Bad Request"
    CONFLICT = "Conflict"
    METHOD_NOT_ALLOWED = "Method not allowed"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    NOT_FOUND = "Not found"
    FORBIDDEN = "Forbidden"
    UNAUTHORIZED = "Unauthorized"
    TOO_MANY_REQUESTS = "You have made too many requests. Please try again later. Retry after {} seconds"
    UNPROCESSABLE = "Unprocessable"

    # Database Error msgs
    DATA_INTEGRITY_CONSTRAINT_VOLIATED = "Data integrity constraint violated."
    DATABASE_TEMPORARILY_UNAVAILABLE = "Database temporarily unavailable."
    DATABASE_ERROR_OCCURRED = "Database error occurred."
    INVALID_DATA_FORMAT = "Invalid data format."
    VALIDATION_FAILED = "Validation Failed."
    CANNOT_DELETE_PROTECTED_RESOURCE = "Cannot delete protected resource."
    DATABASE_OPERATION_NOT_SUPPORRTED = "Database operation not supported."
    DATABASE_PROGRAMMING_ERROR = "Database programming error."

    # Custom Error msgs / Business Logic
    USERNAME_UNAVAILABLE = "Username unavailable"
    USERNAME_NOT_ALLOWED = "Username not allowed"
    EMAIL_MUST_BE_SET = "The given email must be set"

    # Logger msgs
    LOGGER_SETUP = "Setting up logger - objID - {}"
    LOGGING_FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(module)s:%(filename)s:%(funcName)s:%(lineno)d --- %(message)s"

    # Logging Colors
    LOG_GREEN = "\x1b[1;32m"
    LOG_GREY = "\x1b[38;20m"
    LOG_YELLOW = "\x1b[33;20m"
    LOG_RED = "\x1b[31;20m"
    LOG_BOLD_RED = "\x1b[31;1m"
    LOG_RESET = "\x1b[0m"

    # Redis msgs
    REDIS_CONNECTION_SUCCESS = "Successfully connected to Redis!"
    REDIS_CANNOT_CONNECTION = "Could not connect to Redis."
    MY_KEY = "mykey"
    HELLO_REDIS = "hello redis"
    RETRIEVED_VALUE = "Retrieved value:"
    REDIS_CONNECTION_ERROR = "Redis connection error:"
    UNEXPECTED_ERROR_REDIS = "An unexpected error occurred:"

    # Other strings in Application
    ADMIN_USER_ALREADY_REGISTERED = "Admin user already registered"
    ADMIN_USER_REGISTERED = "Admin user registered"
    ADMIN_USER_NOT_REGISTERED = "Admin user not registered"
    CREATING_ADMIN_USER = "Creating admin user"
    ERROR_IN_ADMIN_EMAIL = "Error in admin email"
    ERROR_IN_ADMIN_PASSWORD = "Error in admin password"
    INVALID_JSON = "Invalid JSON"


F = FILLER


def get_http_response(
    payload=None, status=S.HTTP_200_OK, content_type=F.APPLICATION_JSON
):
    response = HttpResponse(
        json.dumps(payload), status=status, content_type=content_type
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


def generate_password_hash(password, salt):
    return bcrypt.hashpw(password.encode(F.UTF8), salt)


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
