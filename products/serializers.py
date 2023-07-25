from rest_framework import serializers
from products.models import Category, ImageProduct, Product
from utils.upload_images import upload_cloud_image, destroy_cloud_image


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduct
        fields = ["image_url"]


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(method_name="get_images")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "discount",
            "slug",
            "image_url",
        ]
        depth = 1

    def create(self, validated_data: dict):
        image = validated_data.pop("image", None)
        categories = validated_data.pop("categories", None)

        if categories is not None:
            for category in categories:
                category = Category.objects.filter(name__iexact=category["name"])
                category.products.add(product)

        if image is None:
            product = Product.objects.create(**validated_data)
            ImageProduct.objects.create(product=product)
            return product

        else:
            product = Product.objects.create(**validated_data)
            cloudinary_response = upload_cloud_image(image)

            if cloudinary_response is not None:
                ImageProduct.objects.create(
                    image_url=cloudinary_response, product=product
                )
            return product

    def get_images(self, obj: Product):
        image_product = ImageProduct.objects.filter(product=obj).first()
        image = ImageProductSerializer(instance=image_product)
        return image.data["image_url"]

    def update(self, instance: Product, validated_data: dict):
        image = validated_data.pop("image", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if image is not None:
            image_product_db = ImageProduct.objects.get(product=instance)
            if destroy_cloud_image(image_product_db.image_url):
                image_product_db.delete()

            cloudinary_response = upload_cloud_image(image)

            if cloudinary_response is not None:
                ImageProduct.objects.create(
                    image_url=cloudinary_response, product=instance
                )

        instance.save()

        return instance
