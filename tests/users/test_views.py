from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


class TestUserViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.register_url = reverse("register")
        cls.auth_url = reverse("auth")
        cls.users_url = reverse("users")
        cls.profile_url = reverse("profile")

        cls.user_data = {
            "first_name": "user",
            "last_name": "01",
            "email": "user01@example.com",
            "username": "user01",
            "password": "12345",
            "is_superuser": False,
            "is_staff": False,
        }
        cls.user_admin_data = {
            "first_name": "admin",
            "last_name": "01",
            "email": "admin01@example.com",
            "username": "admin01",
            "password": "admin",
            "is_superuser": True,
            "is_staff": True,
        }
        cls.admin_test01 = User.objects.create_user(**cls.user_admin_data)
        cls.user_test01 = User.objects.create_user(**cls.user_data)

        cls.admin_data_request = {
            "username": cls.user_admin_data.get("username"),
            "password": cls.user_admin_data.get("password"),
        }

        cls.user_data_request = {
            "username": cls.user_data.get("username"),
            "password": cls.user_data.get("password"),
        }

        response_admin = cls.client.post(
            path=cls.auth_url,
            data=cls.admin_data_request,
            content_type="application/json",
        )
        response_user = cls.client.post(
            path=cls.auth_url,
            data=cls.user_data_request,
            content_type="application/json",
        )

        cls.token_admin = response_admin.data.get("access")
        cls.token_user = response_user.data.get("access")

        cls.user_details_url_admin = reverse(
            "user_details", kwargs={"user_id": cls.admin_test01.id}
        )
        cls.user_details_url_user = reverse(
            "user_details", kwargs={"user_id": cls.user_test01.id}
        )
        cls.user_details_url_user_not_found = reverse(
            "user_details", kwargs={"user_id": 99999999999999}
        )

        cls.user_data_for_eatch = {
            "first_name": "George",
            "last_name": "Clooney",
            "email": "george@example.com",
            "username": "george_user",
            "password": "12345",
        }

        cls.user_update_data = {
            "email": "george_updated@example.com",
            "username": "george_user_updated",
        }

    def test_cant_create_user_if_already_existing(self):
        response = self.client.post(
            path=self.register_url,
            data=self.user_data_request,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_can_create_a_user(self):
        response = self.client.post(
            path=self.register_url,
            data=self.user_data_for_eatch,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"success": "User created successfully."})

    def test_raise_exception_when_field_is_not_present_in_body(self):
        invalid_user = {}
        response = self.client.post(
            path=self.register_url, data=invalid_user, content_type="application/json"
        )

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

    def test_cant_update_user_missing_token(self):
        response = self.client.patch(
            path=self.user_details_url_user, data=self.user_update_data
        )

        expected_response = "Authentication credentials were not provided."

        self.assertContains(response, expected_response, status_code=401)

    def test_cant_update_user_invalid_token(self):
        response = self.client.patch(
            path=self.user_details_url_user,
            data=self.user_update_data,
            headers={"Authorization": "Bearer sdsddasdadsdsdsd"},
        )

        expected_response = "Given token not valid for any token type"

        self.assertContains(response, expected_response, status_code=401)

    def test_cant_update_user_not_owner_or_admin(self):
        response = self.client.patch(
            path=self.user_details_url_admin,
            data=self.user_update_data,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        expected_response = "You do not have permission to perform this action."

        self.assertContains(response, expected_response, status_code=403)

    def test_cant_update_user_owner(self):
        response = self.client.patch(
            path=self.user_details_url_user,
            data=self.user_update_data,
            headers={"Authorization": f"Bearer {self.token_user}"},
            content_type="application/json",
        )

        expected_response = self.user_update_data

        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(expected_response, response.data)

    def test_cant_update_any_user_to_be_admin(self):
        response = self.client.patch(
            path=self.user_details_url_user,
            data=self.user_update_data,
            headers={"Authorization": f"Bearer {self.token_admin}"},
            content_type="application/json",
        )

        expected_response = self.user_update_data

        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(expected_response, response.data)

    def test_cant_delete_user_missing_token(self):
        response = self.client.delete(path=self.user_details_url_admin)

        expected_response = "Authentication credentials were not provided."
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_delete_user_invalid_token(self):
        response = self.client.delete(
            path=self.user_details_url_admin,
            headers={"Authorization": "Bearer sdsddasdadsdsdsd"},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_delete_user_not_owner_or_admin(self):
        response = self.client.delete(
            path=self.user_details_url_admin,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        expected_response = "You do not have permission to perform this action."
        self.assertContains(response, expected_response, status_code=403)

    def test_cant_not_found_user_to_be_deleted(self):
        response = self.client.delete(
            path=self.user_details_url_user_not_found,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        expected_response = "Not found."
        self.assertContains(response, expected_response, status_code=404)

    def test_can_delete_user_to_owner(self):
        response = self.client.delete(
            path=self.user_details_url_user,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        self.assertEqual(response.status_code, 204)

    def test_can_delete_user_to_admin(self):
        response = self.client.delete(
            path=self.user_details_url_user,
            headers={"Authorization": f"Bearer {self.token_admin}"},
        )

        self.assertEqual(response.status_code, 204)

    def test_cant_see_list_all_users_if_missing_token(self):
        response = self.client.get(path=self.users_url)

        expected_response = "Authentication credentials were not provided."
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_list_all_user_if_invalid_token(self):
        response = self.client.delete(
            path=self.user_details_url_admin,
            headers={"Authorization": "Bearer sdsddasdadsdsdsd"},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_see_list_all_users_if_not_admin(self):
        response = self.client.get(
            path=self.users_url,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        expected_response = "You do not have permission to perform this action."
        self.assertContains(response, expected_response, status_code=403)

    def test_can_list_users_only_to_be_admin(self):
        response = self.client.get(
            path=self.users_url, headers={"Authorization": f"Bearer {self.token_admin}"}
        )

        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, 200)

    def test_cant_see_profile_if_not_authenticated(self):
        response = self.client.get(
            path=self.profile_url,
        )

        expected_response = "Authentication credentials were not provided."
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_see_profile_if_invalid_token(self):
        response = self.client.get(
            path=self.profile_url,
            headers={"Authorization": "Bearer sdsddasdadsdsdsd"},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)

    def test_can_see_self_profile(self):
        response = self.client.get(
            path=self.profile_url,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.status_code, 200)

    def test_can_update_self_profile_successfully(self):
        response = self.client.patch(
            path=self.profile_url,
            data={"first_name": "user_upadated"},
            headers={"Authorization": f"Bearer {self.token_user}"},
            content_type="application/json",
        )

        expected_response = {"first_name": "user_upadated"}

        self.assertIsInstance(response.data, dict)
        self.assertContains(response, "user_upadated", 1, status_code=200)
        self.assertDictContainsSubset(expected_response, response.data)

    def test_cant_delete_self_profile_if_not_authenticated(self):
        response = self.client.delete(
            path=self.profile_url,
        )

        expected_response = "Authentication credentials were not provided."
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_delete_self_profile_if_invalid_token(self):
        response = self.client.delete(
            path=self.profile_url,
            headers={"Authorization": "Bearer sdsddasdadsdsdsd"},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)

    def test_can_delete_self_profile_successfully(self):
        response = self.client.delete(
            path=self.profile_url,
            headers={"Authorization": f"Bearer {self.token_user}"},
        )

        self.assertEqual(response.status_code, 204)
