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


class FILLER:
    # Common or one time / non-context / Single word / Non Space literal
    A = "A"
    ACCESS = "access"
    ADMIN = "admin"
    ADMIN_EMAIL = "ADMIN_EMAIL"
    ADMIN_PASSWORD = "ADMIN_PASSWORD"
    AFTER = "after"
    ANON = "anon"
    APPLICATION_JSON = "application/json"
    BODY = "body"
    CODE = "code"
    CONSUMER = "consumer"
    CREATED = "created"
    DATA = "data"
    DELETED = "deleted"
    ERRORS = "errors"
    EMAIL = "email"
    FIELD = "field"
    FIRST_NAME = "first_name"
    GET_TOKEN = "get_token"
    IS_SUPERUSER = "is_superuser"
    IS_STAFF = "is_staff"
    IS_VERIFIED = "is_verified"
    KEY = "key"
    LAST_NAME = "last_name"
    LOC = "loc"
    METHOD = "method"
    MESSAGE = "message"
    MSG = "msg"
    MYSQL = "mysql"
    NAME = "name"
    PASSWORD = "password"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    PK = "pk"
    RECIEVER = "reciever"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    ROLE = "role"
    SALT = "salt"
    SENDER = "sender"
    SELLER = "seller"
    STATUS = "status"
    SUBJECT = "subject"
    SUCCESS = "success"
    SUPER_ADMIN = "super_admin"
    THROTTLE_LIMIT = "throttle_limit"
    TOKEN = "token"
    TYPE = "type"
    UIDB64 = "uidb64"
    USER = "user"
    USERNAME = "username"
    UUID = "uuid"
    VERSION = "version"
    UPDATED = "updated"
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
    UNAVAILABLE = "Unavailable"

    # Database Error msgs
    DATABASE_INTEGRITY_ERROR = "Data integrity error"
    DATA_INTEGRITY_CONSTRAINT_VOLIATED = "Data integrity constraint violated."
    DATABASE_TEMPORARILY_UNAVAILABLE = "Database temporarily unavailable."
    DATABASE_ERROR_OCCURRED = "Database error occurred."
    DATABASE_DATA_ERROR = "Database data error"
    INVALID_DATA_FORMAT = "Invalid data format."
    INVALID_JSON = "Invalid JSON"
    VALIDATION_FAILED = "Validation Failed."
    CANNOT_DELETE_PROTECTED_RESOURCE = "Cannot delete protected resource."
    DATABASE_OPERATION_NOT_SUPPORRTED = "Database operation not supported."
    DATABASE_PROGRAMMING_ERROR = "Database programming error."

    # Custom Error msgs / Business Logic
    USERNAME_UNAVAILABLE = "Username unavailable"
    USERNAME_NOT_ALLOWED = "Username not allowed"
    EMAIL_MUST_BE_SET = "The given email must be set"
    EMAIL_ALREADY_TAKEN = "The given email is already registered"
    EMAIL_NOT_FOUND = "The given email doesn't exist in our system"
    USER_NOT_FOUND = "The given user doesn't exist in our system"
    INCORRECT_CREDENTIALS = "Incorrect credentials"
    INVALID_ROLE = "Role should have these values {}"
    INVALID_USER = "Invalid user"
    INVALID_RESET_TOKEN = "Invalid reset token"
    NEW_PASSWORD_CANNOT_BE_SAME_AS_CURRENT_PASSWORD = "New password can't be same as current password"

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

    # Token related error
    TOKEN_ERROR = "TOKEN_ERROR"
    INVALID_TOKEN = "INVALID_TOKEN"
    EXPIRED_TOKEN = "EXPIRED_TOKEN"
    TOKEN_BACKEND_ERROR = "TOKEN_BACKEND_ERROR"
    TOKEN_BACKEND_EXPIRED_ERROR = "TOKEN_BACKEND_EXPIRED_ERROR"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"

    # Headers
    X_RATELIMIT_LIMIT = "X-RateLimit-Limit"
    X_RATELIMIT_REMAINING = "X-RateLimit-Remaining"
    X_RATELIMIT_RESET = "X-RateLimit-Reset"


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
        json.dumps({F.STATUS: status, F.MESSAGE: message, F.DATA: payload}),
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
    return f""" Reset password : {FRONT_URL}/verify/{uidb64}/{token} """
