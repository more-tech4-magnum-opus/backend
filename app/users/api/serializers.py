from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "about",
            "name",
            "type",
            "telegram",
            "password",
            "salary",
            "respect",
            "wallet_public_key",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "wallet_public_key": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data, username=validated_data["telegram"]
        )
        return user
