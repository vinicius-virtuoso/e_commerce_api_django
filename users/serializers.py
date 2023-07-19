from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_superuser",
            "password",
        ]
        depth = 1
        extra_kwargs = {
            "password": {"write_only": True},
            "is_superuser": {"read_only": True},
            "email": {"required": True},
        }
