import unittest
from django.test import Client
from rest_framework import status

class SimpleTest(unittest.TestCase):
    def test_index_get(self):
        client = Client()
        response = client.get("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_index_put(self):
        client = Client()
        response = client.put("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_index_post(self):
        client = Client()
        response = client.post("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_index_delete(self):
        client = Client()
        response = client.delete("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_index_patch(self):
        client = Client()
        response = client.patch("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_index_options(self):
        client = Client()
        response = client.options("/api/v1")
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_index_error(self):
        client = Client()
        response = client.get("/api/v1/error/401")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_index_raise_error(self):
        client = Client()
        response = client.get("/api/v1/raise-error")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_index(self):
        client = Client()
        response = client.get("/customer/index/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)