from django.test import TestCase, Client
from django.urls import reverse
from users.views import UserCreateView


class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "first_name": "George",
            "last_name": "Clooney",
            "email": "george@example.com",
            "username": "george_user",
            "password": "12345",
        }

    def test_can_create_a_user(self):
        response = self.client.post(path=self.register_url, data=self.user_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"success": "User created successfully."})

    def test_raise_exception_when_field_is_not_present_in_body(self):
        self.user_data.pop("username")
        self.user_data.pop("email")
        invalid_user = self.user_data
        
        response = self.client.post(path=self.register_url, data=invalid_user)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "username": ["This field is required."],
                "email": ["This field is required."],
            },
        )
