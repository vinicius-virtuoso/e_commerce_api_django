from django.db import models

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=190)
  price = models.DecimalField(max_digits=11, decimal_places=2)
  description = models.CharField(max_length=255)
  stock = models.IntegerField(default=1)
  discount = models.IntegerField(default=0)
  

class Category(models.Model):
  name = models.CharField(max_length=100)
  product = models.ManyToManyField('products.Product', related_name='product')
  

class ImageProduct(models.Model):
  image_url = models.CharField(max_length=255)
  product = models.ForeignKey('products.Product',on_delete=models.CASCADE, related_name="image_product")
  
  class Meta:
    db_table = "image_product"