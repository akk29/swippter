import unittest
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from rest_framework.exceptions import Throttled, AuthenticationFailed
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from app.core.exceptions import (
    BadRequestError,
    ConflitError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    MethodNotAllowedError,
    UnprocessableError,
    ExceptionGenerator,
    ServiceUnavailableError,
    Exception500,
    process_library_exceptions,
)

class ExceptionTest(unittest.TestCase):

    def test_bad_request_exception(self):
        try:
            raise BadRequestError()
        except BadRequestError as e:
            self.assertEqual(BadRequestError, type(e))

    def test_unauthorized_exception(self):
        try:
            raise UnauthorizedError()
        except UnauthorizedError as e:
            self.assertEqual(UnauthorizedError, type(e))

    def test_forbidden_exception(self):
        try:
            raise ForbiddenError()
        except ForbiddenError as e:
            self.assertEqual(ForbiddenError, type(e))

    def test_not_found_exception(self):
        try:
            raise NotFoundError()
        except NotFoundError as e:
            self.assertEqual(NotFoundError, type(e))

    def test_method_not_allowed_exception(self):
        try:
            raise MethodNotAllowedError()
        except MethodNotAllowedError as e:
            self.assertEqual(MethodNotAllowedError, type(e))

    def test_unprocessable_exception(self):
        try:
            raise UnprocessableError()
        except UnprocessableError as e:
            self.assertEqual(UnprocessableError, type(e))

    def test_exception_500(self):
        Exception500("")

    def test_throttled(self):
        process_library_exceptions(Throttled(wait=5), "")

    def test_conflict(self):
        try:
            raise ConflitError()
        except ConflitError as e:
            self.assertEqual(ConflitError, type(e))

    def test_service_unavailable(self):
        try:
            raise ServiceUnavailableError()
        except ServiceUnavailableError as e:
            self.assertEqual(ServiceUnavailableError, type(e))

    def test_exception_generator(self):
        ExceptionGenerator.error_generator()

    def test_database_error(self):
        process_library_exceptions(DatabaseError(), "")

    def test_django_error(self):
        process_library_exceptions(PermissionDenied(), "")

    def test_jwt_error(self):
        process_library_exceptions(ExpiredTokenError(), "")

    def test_rest_framework_error(self):
        process_library_exceptions(AuthenticationFailed(), "")
