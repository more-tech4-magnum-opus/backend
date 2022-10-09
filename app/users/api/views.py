from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsAdmin
from users.api.serializers import (
    UserSerializer,
    DepartmentSerializer,
    StreamSerializer,
    CommandSerializer,
    CreateSeasonSerializer,
    ClanSerializer,
)
from users.models import User, Department, Stream, Command, Clan


class ListCreateUserApi(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()


class CreateSeasonApi(generics.CreateAPIView):
    serializer_class = CreateSeasonSerializer
    # permission_classes = [IsAuthenticated, IsAdmin]


class RetrieveUpdateDeleteUserApi(generics.RetrieveUpdateDestroyAPIView):
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


class RetrieveUpdateDeleteDepartmentApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Department.objects.all()


class ListCreateStreamApi(ListCreateDepartmentApi):
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()


class RetrieveUpdateDeleteStreamApi(RetrieveUpdateDeleteDepartmentApi):
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()


class ListCreateCommandApi(ListCreateDepartmentApi):
    serializer_class = CommandSerializer
    queryset = Command.objects.all()


class RetrieveUpdateDeleteCommandApi(RetrieveUpdateDeleteDepartmentApi):
    serializer_class = CommandSerializer
    queryset = Command.objects.all()


class ListClansApiView(generics.ListAPIView):
    serializer_class = ClanSerializer
    queryset = Clan.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]


class GetSelfUserApi(generics.RetrieveAPIView):
    def get_object(self):
        return self.request.user

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
