from users.models import User
from django.test import TestCase


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "first_name": "George",
            "last_name": "Clooney",
            "email": "george@example.com",
            "username": "george_user",
            "password": "12345",
        }

        cls.user = User.objects.create_user(**cls.user_data)

    def test_first_name_max_length(self):
        max_length = self.user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 150)

    def test_last_name_max_length(self):
        max_length = self.user._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 150)

    def test_get_full_name(self):
        result = self.user.get_full_name()
        expected = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(result, expected)

    def test_user_fields(self):
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.username, self.user_data["username"])
