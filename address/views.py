from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.serializires import AddressSerializer


class AddressCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class AddressDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
