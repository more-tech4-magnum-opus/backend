from rest_framework import serializers
from ..service import create_season
from users.models import User
from users.models import User, Department, Stream, Command


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
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "wallet_public_key": {"read_only": True},
            "department": {"read_only": True},
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
        return {'created': True}


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
