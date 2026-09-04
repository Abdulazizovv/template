from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class MeViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="strong-pass-123")
        self.token = Token.objects.get(user=self.user)

    def test_requires_authentication(self):
        resp = self.client.get(reverse("api-user-me"))
        self.assertEqual(resp.status_code, 401)

    def test_returns_own_profile_when_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        resp = self.client.get(reverse("api-user-me"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["username"], "alice")
