from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsAdmin
from users.api.serializers import UserSerializer, CreateSeasonSerializer
from users.models import User


class ListCreateUserApi(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()


class CreateSeasonApi(generics.CreateAPIView):
    serializer_class = CreateSeasonSerializer
    #permission_classes = [IsAuthenticated, IsAdmin]
