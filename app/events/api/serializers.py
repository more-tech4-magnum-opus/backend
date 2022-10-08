from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from events.models import Event, EventAttendance
from users.api.serializers import UserSerializer
from users.models import User


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


class EventAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendance
        fields = ["id", "event_slug", "worker_username", "attended"]
        extra_kwargs = {
            "id": {"read_only": True},
            "event_slug": {"read_only": True},
            "worker_username": {"read_only": True},
            "attended": {"read_only": True},
        }

    def create(self, validated_data):
        return EventAttendance.objects.get_or_create(
            worker=self.context["request"].user,
            event=get_object_or_404(
                Event, slug=self.context["request"].parser_context["kwargs"]["slug"]
            ),
        )[0]


class SubmitUserAttendedSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)

    def create(self, validated_data):
        event = get_object_or_404(
            Event, slug=self.context["request"].parser_context["kwargs"]["slug"]
        )
        ea = EventAttendance.objects.get_or_create(
            event=event,
            worker=get_object_or_404(User, username=validated_data["username"]),
        )[0]
        if not ea.attended:
            ea.attended = True
            ea.save()
            ea.event.attended += 1
            ea.event.save()
        return ea

    def update(self, instance, validated_data):
        pass
