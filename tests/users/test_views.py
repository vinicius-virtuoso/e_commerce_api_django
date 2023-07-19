from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.auth_url = reverse("auth")

        self.user_data = {
            "first_name": "user",
            "last_name": "01",
            "email": "user01@example.com",
            "username": "user01",
            "password": "12345",
            "is_superuser": False,
            "is_staff": False,
        }
        self.user_admin_data = {
            "first_name": "admin",
            "last_name": "01",
            "email": "admin01@example.com",
            "username": "admin01",
            "password": "admin",
            "is_superuser": True,
            "is_staff": True,
        }
        self.admin_test01 = User.objects.create_user(**self.user_admin_data)
        self.user_test01 = User.objects.create_user(**self.user_data)

        self.admin_data_request = {
            "username": self.user_admin_data.get("username"),
            "password": self.user_admin_data.get("password"),
        }

        self.user_data_request = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("password"),
        }

        response_admin = self.client.post(
            path=self.auth_url, data=self.admin_data_request
        )
        response_user = self.client.post(
            path=self.auth_url, data=self.user_data_request
        )

        self.token_admin = response_admin.data.get("access")
        self.token_user = response_user.data.get("access")

        self.user_details_url_admin = reverse(
            "user_details", kwargs={"user_id": self.admin_test01.id}
        )
        self.user_details_url_user = reverse(
            "user_details", kwargs={"user_id": self.user_test01.id}
        )
        self.user_details_url_user_not_found = reverse(
            "user_details", kwargs={"user_id": 99999999999999}
        )
        

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data_for_eatch = {
            "first_name": "George",
            "last_name": "Clooney",
            "email": "george@example.com",
            "username": "george_user",
            "password": "12345",
        }

    def test_can_create_a_user(self):
        response = self.client.post(
            path=self.register_url, data=self.user_data_for_eatch
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"success": "User created successfully."})

    def test_raise_exception_when_field_is_not_present_in_body(self):
        invalid_user = {}
        response = self.client.post(path=self.register_url, data=invalid_user)

        expected_response = {
            "username": ["This field may not be blank.", "This field is required."],
            "password": ["This field may not be blank.", "This field is required."],
        }

        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data["username"][0], expected_response["username"])
        self.assertIn(response.data["password"][0], expected_response["password"])

    def test_can_raise_exception_unauthenticated(self):
        response = self.client.get(
            path=self.user_details_url_admin, headers={"Authorization": f'{" "}'}
        )

        expected_response = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response)

    def test_invalid_token_response(self):
        response = self.client.get(
            path=self.user_details_url_admin,
            headers={"Authorization": "Bearer sdsddasdadsdsdsd"},
        )

        expected_response = "Given token not valid for any token type"

        self.assertContains(response, expected_response, status_code=401)

    def test_user_cant_see_details_not_is_owner_or_admin(self):
        response = self.client.get(
            path=self.user_details_url_admin,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        expected_response = "You do not have permission to perform this action."

        self.assertContains(response, expected_response, status_code=403)

    def test_can_see_any_user_details_to_admin(self):
        response = self.client.get(
            path=self.user_details_url_user,
            headers={"Authorization": f"Bearer {self.token_admin}"},
        )

        expected_response_id = self.user_test01.id
        expected_response_username = self.user_test01.username

        self.assertContains(response, expected_response_id, status_code=200)
        self.assertContains(response, expected_response_username, status_code=200)

    def test_user_not_found_or_deleted(self):
        response = self.client.get(
            path=self.user_details_url_user_not_found,
            headers={"Authorization": f"Bearer {self.token_admin}"},
        )
        expected_response = "Not found."

        self.assertContains(response, expected_response, status_code=404)