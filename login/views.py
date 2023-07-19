from login.serializers import CustomJWTSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
