import json
import unittest
import random
from django.test import Client
from rest_framework import status as S
class RequestIdHeaderTest(unittest.TestCase):
     
     def setUp(self):
        self.client = Client()
        self.random_email = f"signin_test_{random.randint(1000, 9999)}@example.com"
        self.password = "test@1234"
        self.signup_data = {
            "role": 3,
            "email": self.random_email,
            "first_name": "Test",
            "last_name": "User",
            "password": self.password,
        }
        self.invalid_signup_data = {
            "role": 0,
            "email": "self.random_email@email.com",
            "first_name": "Test",
            "last_name": "User",
            "password": self.password,
        }

     def test_header_id(self):
        response = self.client.post("/api/v1/signup", data=json.dumps(self.signup_data), content_type="application/json")
        self.assertEqual(response.status_code, S.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        response_headers = response.headers
        self.assertIn("request_id", response_data)
        self.assertEqual(response_data["request_id"],response_headers["X-Request-Id"])