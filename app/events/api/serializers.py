from rest_framework import serializers

from events.models import Event
from users.api.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = [
            "name",
            "about",
            "slug",
            "creator",
            "starts",
            "image",
            "planning",
            "attended",
        ]
        extra_kwargs = {
            "slug": {"read_only": True},
            "creator": {"read_only": True},
            "planning": {"read_only": True},
            "attended": {"read_only": True},
        }

    def create(self, validated_data):
        return Event.objects.create(
            **validated_data, creator=self.context["request"].user
        )
