from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class OrderPermissionTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@test.com",
            username="user1",
            password="password123"
        )

        self.user2 = User.objects.create_user(
            email="user2@test.com",
            username="user2",
            password="password123"
        )

    def test_user_can_login(self):
        response = self.client.post(
            "/api/token/",
            {
                "email": "user1@test.com",
                "password": "password123"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)