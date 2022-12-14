from rest_framework import serializers
from ..services import create_season
from users.models import User, Department, Stream, Command, Clan


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
            "command",
            "department",
            "clan_name",
            "money",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "wallet_public_key": {"read_only": True},
            "clan_name": {"read_only": True},
            "department": {"read_only": True},
            "money": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data, username=validated_data["telegram"]
        )
        return user


class CreateSeasonSerializer(serializers.Serializer):
    created = serializers.BooleanField(read_only=True)

    def create(self, *args, **kwargs):
        create_season()
        return {"created": True}

    def update(self, instance, validated_data):
        pass


class CommandSerializer(serializers.ModelSerializer):
    workers = UserSerializer(many=True)

    class Meta:
        model = Command
        fields = ["id", "name", "stream", "workers"]
        extra_kwargs = {
            "id": {"read_only": True},
            "stream": {"write_only": True},
            "workers": {"read_only": True},
        }


class StreamSerializer(serializers.ModelSerializer):
    commands = CommandSerializer(many=True)

    class Meta:
        model = Stream
        fields = ["id", "name", "department", "commands"]
        extra_kwargs = {
            "id": {"read_only": True},
            "department": {"write_only": True},
            "commands": {"read_only": True},
        }


class DepartmentSerializer(serializers.ModelSerializer):
    streams = StreamSerializer(many=True)

    class Meta:
        model = Department
        fields = ["id", "name", "streams"]
        extra_kwargs = {
            "id": {"read_only": True},
            "streams": {"read_only": True},
        }


class ClanSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Clan
        fields = ["name", "users"]
