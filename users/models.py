from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(max_length=180, unique=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
