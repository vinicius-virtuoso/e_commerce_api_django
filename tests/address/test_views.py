from django.test import TestCase, Client
from address.models import Address
from users.models import User
from django.urls import reverse


class TestAddress(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.address_url = reverse("address")
        cls.login_url = reverse("auth")

        cls.user_data = {
            "first_name": "user",
            "last_name": "01",
            "email": "user01@example.com",
            "username": "user01",
            "password": "12345",
            "is_superuser": False,
            "is_staff": False,
        }

        cls.user_data_without_address = {
            "first_name": "user",
            "last_name": "02",
            "email": "user02@example.com",
            "username": "user02",
            "password": "12345",
            "is_superuser": False,
            "is_staff": False,
        }

        cls.user_without_address = User.objects.create_user(
            **cls.user_data_without_address
        )
        cls.user_created = User.objects.create_user(**cls.user_data)

        cls.address_data = {
            "state": "SC",
            "city": "Florianópolis",
            "neighbourhood": "Jardim Atlantico",
            "street": "Luis Carlos Prestes",
            "zip_code": "88090250",
            "number": 172,
            "complement": "Casa",
        }
        cls.address_created = Address.objects.create(
            **cls.address_data, user=cls.user_created
        )

        response = cls.client.post(
            path=cls.login_url,
            data={
                "username": cls.user_data["username"],
                "password": cls.user_data["password"],
            },
            content_type="application/json",
        )

        response_without_address = cls.client.post(
            path=cls.login_url,
            data={
                "username": cls.user_data_without_address["username"],
                "password": cls.user_data_without_address["password"],
            },
            content_type="application/json",
        )

        cls.token = response.data["access"]
        cls.token_user_without_address = response_without_address.data["access"]

    def test_cant_create_address_if_not_authenticated(self):
        response = self.client.post(
            path=self.address_url,
            data=self.address_data,
            content_type="application/json",
        )

        expected_response = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response)

    def test_cant_create_address_if_already_existing(self):
        response = self.client.post(
            path=self.address_url,
            data=self.address_data,
            content_type="application/json",
            headers={"Authorization": "Bearer " + self.token},
        )

        expected_response = "Address has already been added to this user."
        self.assertContains(response, expected_response, status_code=400)

    def test_cant_create_address_if_token_is_invalid(self):
        response = self.client.post(
            path=self.address_url,
            data=self.address_data,
            content_type="application/json",
            headers={"Authorization": "Bearer ssssssssssssssasasa"},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_create_address_if_invalid_fields(self):
        invalid_address = {}

        response = self.client.post(
            path=self.address_url,
            data=invalid_address,
            content_type="application/json",
            headers={"Authorization": "Bearer " + self.token},
        )

        expected_response = {
            "state": ["This field may not be blank.", "This field is required."],
            "city": ["This field may not be blank.", "This field is required."],
            "neighbourhood": [
                "This field may not be blank.",
                "This field is required.",
            ],
            "street": ["This field may not be blank.", "This field is required."],
            "zip_code": ["This field may not be blank.", "This field is required."],
            "number": ["This field may not be blank.", "This field is required."],
            "complement": ["This field may not be blank.", "This field is required."],
        }

        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data["state"][0], expected_response["state"])
        self.assertIn(response.data["city"][0], expected_response["city"])
        self.assertIn(
            response.data["neighbourhood"][0], expected_response["neighbourhood"]
        )
        self.assertIn(response.data["street"][0], expected_response["street"])
        self.assertIn(response.data["number"][0], expected_response["number"])
        self.assertIn(response.data["complement"][0], expected_response["complement"])

    def test_cant_create_address_if_invalid_state_choice(self):
        invalid_state_address = self.address_data
        invalid_state_address["state"] = "FFFDDA"

        response = self.client.post(
            path=self.address_url,
            data=invalid_state_address,
            content_type="application/json",
            headers={"Authorization": "Bearer " + self.token},
        )

        expected_response = "is not a valid choice."
        self.assertContains(response, expected_response, status_code=400)

    def test_can_create_address(self):
        response = self.client.post(
            path=self.address_url,
            data=self.address_data,
            content_type="application/json",
            headers={"Authorization": "Bearer " + self.token_user_without_address},
        )

        expected_response = {
            "state": "SC",
            "city": "Florianópolis",
            "neighbourhood": "Jardim Atlantico",
            "street": "Luis Carlos Prestes",
            "zip_code": "88090250",
            "number": 172,
            "complement": "Casa",
        }

        self.assertDictContainsSubset(expected_response, response.data)
        self.assertEqual(response.status_code, 201)

    def test_cant_update_address_is_not_authenticated(self):
        response = self.client.patch(
            path=self.address_url,
            data={"street": "Rua de update"},
            content_type="application/json",
        )

        expected_response = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response)

    def test_cant_update_address_if_invalid_token(self):
        response = self.client.patch(
            path=self.address_url,
            data={"street": "Rua de update"},
            content_type="application/json",
            headers={"Authorization": "Bearer ssssssssssssssasasa"},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_update_address_if_not_found(self):
        response = self.client.patch(
            path=self.address_url,
            data={"street": "Rua de update"},
            content_type="application/json",
            headers={"Authorization": "Bearer " + self.token_user_without_address},
        )

        expected_response = {"detail": "Not found."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)

    def test_cant_update_address_if_invalid_state(self):
        invalid_state_address = self.address_data
        invalid_state_address["state"] = "FFFDDA"

        response = self.client.patch(
            path=self.address_url,
            data=invalid_state_address,
            content_type="application/json",
            headers={"Authorization": "Bearer " + self.token},
        )

        expected_response = "is not a valid choice."
        self.assertContains(response, expected_response, status_code=400)

    def test_cant_update_address_successfully(self):
        response = self.client.patch(
            path=self.address_url,
            data={"street": "Rua de update"},
            content_type="application/json",
            headers={"Authorization": "Bearer " + self.token},
        )

        expected_response = {"street": "Rua de update"}
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(expected_response, response.data)

    def test_cant_delete_address_if_not_authenticated(self):
        response = self.client.delete(path=self.address_url)

        expected_response = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response)

    def test_cant_delete_address_if_invalid_token(self):
        response = self.client.delete(
            path=self.address_url,
            headers={"Authorization": "Bearer ssssssssssssssasasa"},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)

    def test_cant_delete_address_if_not_found(self):
        response = self.client.delete(
            path=self.address_url,
            headers={"Authorization": "Bearer " + self.token_user_without_address},
        )

        expected_response = {"detail": "Not found."}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)

    def test_can_delete_address_successfully(self):
        response = self.client.delete(
            path=self.address_url,
            headers={"Authorization": "Bearer " + self.token},
        )

        self.assertEqual(response.status_code, 204)
