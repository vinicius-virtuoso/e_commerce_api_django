# Generated by Django 4.2.3 on 2023-07-19 16:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(max_length=180, unique=True),
        ),
    ]