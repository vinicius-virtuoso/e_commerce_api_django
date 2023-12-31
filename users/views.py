from rest_framework.views import APIView, Response, Request, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import OnwerOrAdmin
from users.models import User
from users.serializers import UserSerializer


class UserCreateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(
                {"success": "User created successfully."}, status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, OnwerOrAdmin]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"


class ListUsersView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        return user
