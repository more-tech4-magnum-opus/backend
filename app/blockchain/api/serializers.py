from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from users.models import User


class TransactFromAdminSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    amount = serializers.IntegerField(validators=[MinValueValidator(1)])

    def validate_username(self, val):
        return get_object_or_404(User, username=val)


class TransactToAdminSerializer(serializers.Serializer):
    amount = serializers.IntegerField(validators=[MinValueValidator(1)])
