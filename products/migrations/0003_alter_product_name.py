# Generated by Django 4.2.3 on 2023-07-24 21:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_alter_imageproduct_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=190, unique=True),
        ),
    ]
