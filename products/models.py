from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=190)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    slug = models.CharField(max_length=250, unique=True)


class ImageProduct(models.Model):
    image_url = models.CharField(
        default="https://res.cloudinary.com/dnkw0zu2x/image/upload/v1688328201/django_commerce/no-photo.png",
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="image_product"
    )

    class Meta:
        db_table = "image_product"


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField("products.Product", related_name="products")
