import unittest
from django.test import Client
from rest_framework import status

class AdminTest(unittest.TestCase):
    
    def test_admin(self):
        client = Client()
        response = client.get("/admin")
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_admin_login(self):
        client = Client()
        response = client.get("/admin/login/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    