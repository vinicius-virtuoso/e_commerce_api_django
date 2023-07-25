from django.test import TestCase, Client
from django.urls import reverse
from users.models import User


class TestLoginViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.login_url = reverse("auth")

        cls.invalid_user = {
            "username": "invalid_user",
            "password": "99999999999999999",
        }
        cls.required_fields = {"password": "99999999999999999"}
        cls.fields_blank = {"username": "", "password": ""}

        cls.user_data = {
            "first_name": "George",
            "last_name": "Clooney",
            "email": "george@example.com",
            "username": "george_user",
            "password": "12345",
        }
        
        cls.user_credentials_invalid = {
            
        }

        cls.user = User.objects.create_user(**cls.user_data)
        
    def test_cant_returnt_if_incorrect_password(self):
        user = {"username": "george_user", "password": "32141414"}
        response = self.client.post(path=self.login_url, data=user)
        
        expected_response = "No active account found with the given credentials"
        self.assertContains(response, expected_response, status_code=401)
        
        

    def test_can_returned_token_jwt(self):
        user = {"username": "george_user", "password": "12345"}
        response = self.client.post(path=self.login_url, data=user)

        self.assertContains(response, "access", status_code=200)
        

    def test_can_raise_returned_unauthorized(self):
        response = self.client.post(path=self.login_url, data=self.invalid_user)

        self.assertContains(response, "detail", status_code=401)
        self.assertContains(
            response,
            "No active account found with the given credentials",
            status_code=401,
        )

    def test_can_raise_error_field_or_fields_required(self):
        response = self.client.post(path=self.login_url, data=self.fields_blank)

        expected_response = {
            "username": ["This field may not be blank.", "This field is required."],
            "password": ["This field may not be blank.", "This field is required."],
        }

        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data["username"][0], expected_response["username"])
        self.assertIn(response.data["password"][0], expected_response["password"])
