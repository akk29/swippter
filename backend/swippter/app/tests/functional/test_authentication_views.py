import json
import unittest
import random
from django.test import Client
from rest_framework import status as S
from app.dao.user_dao import UserDAO
from app.utils.utilities import F
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.management import call_command
from app.core.celery_tasks import trigger_mail_backround

class SimpleTest(unittest.TestCase):

    def setUp(self):
        """Set up test data that can be accessed by all test methods"""
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
        self.signin_data = {
            "email": self.random_email,
            "password": self.password,
        }
        self.forgot_password_data = {
            "email": self.random_email,
        }
        self.user_dao = UserDAO.get_instance()
        
    def test_signup_failure(self):
        """Test signup endpoint with invalid credentials"""
        signup_data = {
            "email": "invalid_email",
            "password": self.password,
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post("/api/v1/signup", data=json.dumps(signup_data), content_type="application/json")
        self.assertEqual(response.status_code, S.HTTP_422_UNPROCESSABLE_ENTITY)
        response_data = json.loads(response.content)
        self.assertIn("errors", response_data)

    def test_user_success(self):
        '''Test user signup using valid data '''
        # First, sign up a user
        signup_response = self.client.post("/api/v1/signup", data=json.dumps(self.signup_data), content_type="application/json")
        self.assertEqual(signup_response.status_code, S.HTTP_201_CREATED)
        
        '''Test already signed up user'''
        signup_response = self.client.post("/api/v1/signup", data=json.dumps(self.signup_data), content_type="application/json")
        self.assertEqual(signup_response.status_code, S.HTTP_422_UNPROCESSABLE_ENTITY)

        """Test signin endpoint with valid credentials"""
        # Then, test signin with the same credentials
        response = self.client.post("/api/v1/signin", data=json.dumps(self.signin_data), content_type="application/json")
        self.assertEqual(response.status_code, S.HTTP_200_OK)
        signin_response_data = json.loads(response.content)
        self.assertIn("data", signin_response_data)
        self.assertIn("token", signin_response_data["data"])
        self.assertIn("access", signin_response_data["data"]["token"])
        self.assertIn("refresh", signin_response_data["data"]["token"])
        token = signin_response_data["data"]["token"]["access"]

        """Test signin endpoint with invalid credentials"""
        response = self.client.post("/api/v1/signin", data=json.dumps({
            "email": self.random_email,
            "password": "wrongpassword",
        }), content_type="application/json")
        self.assertEqual(response.status_code, S.HTTP_401_UNAUTHORIZED)

        """Test forgot password endpoint with valid credentials"""
        response = self.client.post("/api/v1/forgot", data=json.dumps(self.forgot_password_data), content_type="application/json")
        self.assertEqual(response.status_code, S.HTTP_200_OK)
        self.assertIn(response.status_code, [S.HTTP_200_OK])

        user = self.user_dao.fetch_one(**{F.EMAIL : self.random_email})
        uidb64 = urlsafe_base64_encode(force_bytes(user.uuid))
        _token = default_token_generator.make_token(user)
        verify_token_url = f'/api/v1/verify-token/{uidb64}/{_token}'
        response = self.client.get(verify_token_url)
        self.assertEqual(response.status_code, S.HTTP_200_OK)

        """SUCCESS:Test user change password using valid token"""
        response = self.client.post("/api/v1/change-password", data=json.dumps({
            "password": "new_password@123",
        }), content_type="application/json",headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, S.HTTP_200_OK)
        self.assertIn(response.status_code, [S.HTTP_200_OK])
        
        """FAILURE:Test user change password using invalid token"""
        response = self.client.post("/api/v1/change-password", data=json.dumps({
            "password": "new_password@123",
        }), content_type="application/json",headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, S.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_signup_failure_invalid_data(self):
        """Test signup endpoint with invalid data"""
        response = self.client.post("/api/v1/signup", data=json.dumps(self.invalid_signup_data), content_type="application/json")
        self.assertEqual(response.status_code, S.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_signin_failure_user_not_found(self):
        """Test signin endpoint with invalid credentials"""
        signin_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post("/api/v1/signin", data=json.dumps(signin_data), content_type="application/json")
        # Should return an error status (likely 400 or 401)
        self.assertIn(response.status_code, [S.HTTP_400_BAD_REQUEST, S.HTTP_401_UNAUTHORIZED])
        
    def test_forgot_password_failure(self):
        """Test forgot password endpoint with invalid credentials"""
        forgot_password_data = {
            "email": "invalid_email@email.com",
        }
        response = self.client.post("/api/v1/forgot", data=json.dumps(forgot_password_data), content_type="application/json")
        self.assertEqual(response.status_code, S.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn(response.status_code, [S.HTTP_422_UNPROCESSABLE_ENTITY])

    def test_create_admin_command(self):
        """ Test create admin command."""
        args = []
        opts = {}
        call_command('create_admin', *args, **opts)


    def test_shared_task(self):
        kwargs = {
            F.EMAIL : "a@a.com",
            F.MESSAGE : "msg",
            F.SENDER : "sender",
            F.RECIEVER : "receiver"
        }
        trigger_mail_backround(**kwargs)