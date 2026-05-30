from django.urls import reverse
from rest_framework.test import APITestCase


class AuthAPITest(APITestCase):

    def test_register_user(self):
        response = self.client.post("/api/auth/register/", {
            "email": "client@test.com",
            "username": "client1",
            "first_name": "Client",
            "last_name": "Test",
            "phone_number": "+60123456789",
            "password": "password123"
        }, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], "client@test.com")