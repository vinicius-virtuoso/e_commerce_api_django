from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from products.models import ImageProduct, Product
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from users.models import User


class TestProductViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product_create_url = reverse("product_create")
        cls.catalog_products_url = reverse("products_catalog")
        cls.auth_url = reverse("auth")
        cls.client = APIClient()
        
        user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="12345",
            is_staff=False,
            is_superuser=False,
        )
        admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="12345",
            is_staff=True,
            is_superuser=True,
        )
        
        cls.respose_admin = cls.client.post(
            path=cls.auth_url, data={"username": admin.username, "password": "12345"}
        )
        cls.respose_user = cls.client.post(
            path=cls.auth_url, data={"username": user.username, "password": "12345"}
        )

        cls.user_token = cls.respose_user.data["access"]
        cls.admin_token = cls.respose_admin.data["access"]
        
        cls.invalid_token = "sasasasasasaasasas3342342"
        
        cls.product_updated = {
            "name": "Product updated",
            "price":"199.99",
            "description": "Product description updated",
            "stock": 100,
            "slug": "product_updated",
            "discount": 70,
            # "image": cls.image_file
        }
        
        cls.product_data_invalid_types = {
            "name": "Produto com tipo de campos invalido",
            "price": "sas",
            "description": "Este é um produto já criado.",
            "slug": "product_fields_types_invalids",
            "stock": "aasas",
            "discount": "sasas",
        }

        cls.product_data_negatives_fields = {
            "name": "Produto com tipo de campos negativos",
            "price": "99.99",
            "description": "Este é um produto já criado.",
            "slug": "product_fields_negatives",
            "stock": -333,
            "discount": -333,
        }
        

        cls.products = [
            Product.objects.create(
                name=f"Product Test {product_id}",
                description=f"This is a test product id {product_id}",
                price=199.90,
                slug=f"product_test_{product_id}",
                stock=99,
                discount=0
            )
            for product_id in range(1, 4)
        ]
        
        cls.images_products = [ImageProduct.objects.create(product=product) for product in cls.products]
        
        cls.product_has_been_created_url = reverse(
            "product_details", kwargs={"slug": cls.products[0].slug}
        )
        
        cls.product_has_been_created_url_03 = reverse(
            "product_details", kwargs={"slug": cls.products[2].slug}
        )
        
        cls.product_not_found_url = reverse(
            "product_details", kwargs={"slug": "not_exist"}
        )

        cls.image_path = os.path.join(
            os.path.dirname(__file__), "..", "images", "test_image.png"
        )
        
        with open(cls.image_path, "rb") as f:
            cls.image_file = SimpleUploadedFile(
                "test_image.png", f.read(), content_type="image/png"
            )
        
        cls.product_data_static = {
                "name": "Produto de Teste com imagem",
                "price": "99.99",
                "description": "Descrição do produto de teste.",
                "slug": "product-test_with_image",
                "stock": 10,
                "discount": 0,
                # "image": cls.image_file,
            }

            

        
    
    def test_cant_create_a_product_if_authenticated(self):
        response = self.client.post(
            path=self.product_create_url,
            data=self.product_data_static,
            format="multipart",
            follow=True,
        )

        expected_response = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response)
        
        
        
    def test_cant_create_an_product_if_token_to_be_invalid(self):
        response = self.client.post(
            path=self.product_create_url,
            data=self.product_data_static,
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.invalid_token},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)
        
    def test_cant_create_a_product_if_common_user(self):
        response = self.client.post(
            path=self.product_create_url,
            data=self.product_data_static,
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.user_token},
        )

        expected_response = "You do not have permission to perform this action."
        self.assertContains(response, expected_response, status_code=403)
        
        
    def test_raise_exception_if_field_invalids_in_body(self):
        response = self.client.post(
            path=self.product_create_url,
            data={},
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.admin_token},
        )


        expected_response = {
            "name": ["This field may not be blank.", "This field is required."],
            "price": ["This field may not be blank.", "This field is required."],
            "description": ["This field may not be blank.", "This field is required."],
            "slug": ["This field may not be blank.", "This field is required."],
            "stock": ["This field may not be blank.", "This field is required."]
        }

        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data["name"][0], expected_response["name"])
        self.assertIn(response.data["price"][0], expected_response["price"])
        self.assertIn(response.data["description"][0], expected_response["description"])
        self.assertIn(response.data["slug"][0], expected_response["slug"])
        self.assertIn(response.data["stock"][0], expected_response["stock"])
        
        
    def test_raise_exception_fields_types_invalids(self):
        response = self.client.post(
            path=self.product_create_url,
            data=self.product_data_invalid_types,
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.admin_token},
        )

        expected_response = {
            "price": ["A valid number is required."],
            "stock": ["A valid integer is required."],
            "discount": ["A valid integer is required."]
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected_response)
        
        
    def test_raise_exception_fields_if_negatives(self):
        response = self.client.post(
            path=self.product_create_url,
            data=self.product_data_negatives_fields,
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.admin_token},
        )

        expected_response = {
            "stock": ["Ensure this value is greater than or equal to 0."],
            "discount": ["Ensure this value is greater than or equal to 0."]
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected_response)
        

    def test_cant_create_product_if_already_existing(self):
        
        product = {
            "name": self.products[0].name,
            "price": self.products[0].price,
            "description": self.products[0].description,
            "slug": self.products[0].slug,
            "stock": self.products[0].stock,
            "discount": self.products[0].discount
        }
        
        response = self.client.post(
            path=self.product_create_url,
            data=product,
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.admin_token},
        )

        expected_response = {'detail': 'Product already exists.'}
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data, expected_response)


    def test_can_create_product_successfully(self):
        response = self.client.post(
            path=self.product_create_url,
            data=self.product_data_static,
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.admin_token},
        )
        expected_response = {
            "name": self.product_data_static['name'],
            "price": self.product_data_static['price'],
            "description": self.product_data_static['description'],
            "slug": self.product_data_static['slug'],
            "discount": self.product_data_static['discount'],
            "stock": self.product_data_static['stock'],
        }
        

        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(expected_response, response.data)
        
        

    def test_can_see_catalog_products(self):
        response = self.client.get(path=self.catalog_products_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)


    def test_cant_see_product_detail_if_not_found(self):
        response = self.client.get(path=self.product_not_found_url)

        expected_response = {"detail": "Not found."}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


    def test_can_see_product_detail_successfully(self):
        response = self.client.get(path=self.product_has_been_created_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)




    def test_cant_update_product_if_unauthorized(self):
        response = self.client.patch(
            path=self.product_has_been_created_url, data={"stock": 100}
        )

        expected_response = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response)



    def test_cant_update_product_if_not_admin(self):
        response = self.client.patch(
            path=self.product_has_been_created_url,
            format="multipart",
            follow=True,
            data=self.product_updated,
            headers={"Authorization": "Bearer " + self.user_token},
        )

        expected_response = "You do not have permission to perform this action."
        self.assertContains(response, expected_response, status_code=403)

    def test_cant_update_product_if_not_found(self):
        response = self.client.patch(
            path=self.product_has_been_created_url,
            data=self.product_updated,
            headers={"Authorization": "Bearer " + self.user_token},
        )

        expected_response = "You do not have permission to perform this action."
        self.assertContains(response, expected_response, status_code=403)


    def test_cant_update_product_if_invalid_token(self):
        response = self.client.patch(
            path=self.product_has_been_created_url,
            data=self.product_updated,
            headers={"Authorization": "Bearer " + self.invalid_token},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)
        

    def test_can_update_product_successfully(self):
        response = self.client.patch(
            path=self.product_has_been_created_url,
            data=self.product_updated,
            format="multipart",
            follow=True,
            headers={"Authorization": "Bearer " + self.admin_token},
        )
        
        # self.product_updated.pop('image')
        expected_response = self.product_updated
        
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(expected_response, response.data)



    def test_cant_delete_product_if_unauthorized(self):
        response = self.client.delete(path=self.product_has_been_created_url)

        expected_response = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response)

    def test_cant_delete_product_if_invalid_token(self):
        response = self.client.delete(
            path=self.product_has_been_created_url,
            headers={"Authorization": "Bearer " + self.invalid_token},
        )

        expected_response = "Given token not valid for any token type"
        self.assertContains(response, expected_response, status_code=401)
        

    def test_cant_delete_product_if_not_found(self):
        response = self.client.delete(
            path=self.product_not_found_url,
            headers={"Authorization": "Bearer " + self.admin_token},
        )

        expected_response = {"detail": "Not found."}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)

    def test_cant_delete_product_if_user_commmon(self):
        response = self.client.delete(
            path=self.product_has_been_created_url,
            headers={"Authorization": "Bearer " + self.user_token},
            format="multipart",
            follow=True
        )

        expected_response = "You do not have permission to perform this action."
        self.assertContains(response, expected_response, status_code=403)

    # def test_cant_delete_product_if_existing_orders(self):
    #     response = self.client.delete(
    #         path=self.product_has_been_created_url,
    #         headers={"Authorization": "Bearer " + self.admin_token},
    #     )

    #     expected_response = {"detail": "There are orders related to this product."}
    #     self.assertContains(response, expected_response, status_code=400)
        

    def test_can_delete_product_successfully(self):
        response = self.client.delete(
                path=self.product_has_been_created_url_03,
                headers={"Authorization": "Bearer " + self.admin_token},
                format="multipart",
                follow=True
            )

        self.assertEqual(response.status_code, 204)

