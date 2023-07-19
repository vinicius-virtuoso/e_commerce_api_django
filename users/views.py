from rest_framework.views import APIView, Response, Request
from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserCreateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response({"success": "User created successfully."}, status=201)
        return Response(serializer.errors, status=400)
