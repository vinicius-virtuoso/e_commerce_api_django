from django.test import TestCase
from products.models import Product, Category, ImageProduct


class TestProduct(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = Category.objects.create(name="Exercicios")

        cls.product_data = {
            "name": "Tenis Nike Race",
            "description": "Tenis confortavél para você correr",
            "price": "199.90",
            "stock": 99,
            "discount": 0,
        }

        cls.product_mock = Product.objects.create(**cls.product_data)
        cls.category.products.add(cls.product_mock)

        cls.image_product = ImageProduct.objects.create(product=cls.product_mock)

    def test_product_name_max_length(self):
        name_max_length = self.product_mock._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 190)

    def test_product_description_max_length(self):
        description_max_length = self.product_mock._meta.get_field(
            "description"
        ).max_length
        self.assertEqual(description_max_length, 255)

    def test_slug_max_length(self):
        slug_max_length = self.product_mock._meta.get_field("slug").max_length
        self.assertEqual(slug_max_length, 250)

    def test_product_discount_max_length(self):
        discount_value_default = self.product_mock._meta.get_field("discount").default
        self.assertEqual(discount_value_default, 0)

    def test_category_name_max_length(self):
        name_max_length = self.category._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 100)

    def test_image_product_max_length(self):
        image_default = self.image_product._meta.get_field("image_url").default
        self.assertEqual(image_default, "https://res.cloudinary.com/dnkw0zu2x/image/upload/v1688328201/django_commerce/no-photo.png")
