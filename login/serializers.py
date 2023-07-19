from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        token["email"] = user.email
        token["username"] = user.username
        token["id"] = user.id

        return token
