from rest_framework import serializers
from address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "state",
            "city",
            "neighbourhood",
            "street",
            "zip_code",
            "number",
            "complement",
        ]

    def create(self, validated_data: dict):
        address_exists = Address.objects.filter(user=validated_data["user"]).exists()
        if address_exists:
            raise serializers.ValidationError(
                {"detail": "Address has already been added to this user."}
            )
        address = Address.objects.create(**validated_data)
        return address
