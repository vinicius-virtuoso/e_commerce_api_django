from django.db import IntegrityError
from address.models import Address
from django.test import TestCase

from users.models import User


class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "first_name": "George",
            "last_name": "Clooney",
            "email": "george@example.com",
            "username": "george_user",
            "password": "12345",
        }
        cls.user = User.objects.create_user(**cls.user_data)

        cls.address_data = {
            "state": "SC",
            "street": "Rua Luiz Carlos Prestes",
            "city": "Floarianópolis",
            "zip_code": "88090250",
            "neighbourhood": "Jardim Atlântico",
            "complement": "Casa fundos",
            "number": 171,
            "user": cls.user,
        }

        cls.address = Address.objects.create(**cls.address_data)

    def test_state_max_length(self):
        state_max_length = self.address._meta.get_field("state").max_length
        self.assertEqual(state_max_length, 2)

    def test_street_max_length(self):
        street_max_length = self.address._meta.get_field("street").max_length
        self.assertEqual(street_max_length, 170)

    def test_city_max_length(self):
        city_max_length = self.address._meta.get_field("city").max_length
        self.assertEqual(city_max_length, 100)

    def test_zip_code_max_length(self):
        zip_code_max_length = self.address._meta.get_field("zip_code").max_length
        self.assertEqual(zip_code_max_length, 8)

    def test_number_max_length(self):
        number_max_length = self.address._meta.get_field("number").max_length
        self.assertEqual(number_max_length, None)

    def test_neighbourhood_max_length(self):
        neighbourhood_max_length = self.address._meta.get_field(
            "neighbourhood"
        ).max_length
        self.assertEqual(neighbourhood_max_length, 180)

    def test_complement_max_length(self):
        complement_max_length = self.address._meta.get_field("complement").max_length
        self.assertEqual(complement_max_length, 170)

    def test_address_related_user(self):
        related_user = self.address.user
        expected = self.user
        self.assertEqual(related_user, expected)
        self.assertEqual(related_user.get_username(), expected.get_username())

    def test_if_raise_error_when_address_already_have_an_user(self):
        with self.assertRaises(IntegrityError):
            address_two = Address.objects.create(**self.address_data)
            address_two.user = self.user
            address_two.save()
