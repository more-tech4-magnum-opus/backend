from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsAdmin
from users.api.serializers import (
    UserSerializer,
    DepartmentSerializer,
    StreamSerializer,
    CommandSerializer,
)
from users.models import User, Department, Stream, Command


class ListCreateUserApi(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()


class RetireUpdateDeleteUserApi(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        user = get_object_or_404(
            User,
            username=self.request.parser_context["kwargs"]["username"],
        )
        return user

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()


class ListCreateDepartmentApi(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Department.objects.all()


class RetireUpdateDeleteDepartmentApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Department.objects.all()


class ListCreateStreamApi(ListCreateDepartmentApi):
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()


class RetireUpdateDeleteStreamApi(RetireUpdateDeleteDepartmentApi):
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()


class ListCreateCommandApi(ListCreateDepartmentApi):
    serializer_class = CommandSerializer
    queryset = Command.objects.all()


class RetireUpdateDeleteCommandApi(RetireUpdateDeleteDepartmentApi):
    serializer_class = CommandSerializer
    queryset = Command.objects.all()
