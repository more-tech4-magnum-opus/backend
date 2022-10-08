from datetime import datetime

import pytz
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.permissions import IsManager, IsWorker
from events.api.serializers import (
    EventSerializer,
    EventAttendanceSerializer,
    SubmitUserAttendedSerializer,
)
from events.models import Event, EventAttendance


class ListCreateEventApi(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Event.objects.filter(
        starts__gte=datetime.now(pytz.timezone("Europe/Moscow"))
    )


class RetrieveUpdateDeleteEventApi(generics.RetrieveUpdateDestroyAPIView):
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


class RetrieveSubmitDeleteEventAttendance(
    generics.CreateAPIView, generics.RetrieveDestroyAPIView
):
    """Gets/Submits/Deletes that user is planing to go on event. Only works for worker"""

    def get_object(self):
        event = get_object_or_404(
            Event,
            slug=self.request.parser_context["kwargs"]["slug"],
        )
        if EventAttendance.objects.filter(
            event=event, worker=self.request.user
        ).exists():
            return EventAttendance.objects.get(event=event, worker=self.request.user)
        raise NotFound

    serializer_class = EventAttendanceSerializer
    permission_classes = [IsAuthenticated, IsWorker]


class ListPlannedEvents(generics.ListAPIView):
    """Lists events that worker is planning to attend. Only works for worker"""

    def get_queryset(self):
        return self.request.user.events.filter(
            attended=False,
            event__starts__gte=datetime.now(pytz.timezone("Europe/Moscow")),
        )

    serializer_class = EventAttendanceSerializer
    permission_classes = [IsAuthenticated, IsWorker]


class ListAttendedWorkersApi(generics.ListAPIView):
    def get_queryset(self):
        return EventAttendance.objects.filter(
            event__slug=self.request.parser_context["kwargs"]["slug"]
        )

    serializer_class = EventAttendanceSerializer
    permission_classes = [IsAuthenticated, IsManager]


class SubmitWorkerAttendedEvent(generics.CreateAPIView):
    serializer_class = SubmitUserAttendedSerializer
    permission_classes = [IsAuthenticated, IsManager]
