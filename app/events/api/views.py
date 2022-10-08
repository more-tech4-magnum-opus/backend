from datetime import datetime

import pytz
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsManager
from events.api.serializers import EventSerializer
from events.models import Event


class ListCreateEventApi(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Event.objects.filter(
        starts__gte=datetime.now(pytz.timezone("Europe/Moscow"))
    )


class RetireUpdateDeleteEventApi(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        event = get_object_or_404(
            Event,
            slug=self.request.parser_context["kwargs"]["slug"],
        )
        return event

    serializer_class = EventSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Event.objects.all()
