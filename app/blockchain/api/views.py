from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from blockchain.api.serializers import (
    TransactFromAdminSerializer,
    TransactToAdminSerializer,
)
from blockchain.models import Transaction
from blockchain.services import (
    transact_from_admin,
    transact_to_admin,
    list_user_transactions,
)
from common.permissions import IsAdmin
from utils.blockchain import get_balance


class TransactFromAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(request_body=TransactFromAdminSerializer)
    def post(self, request):
        serializer = TransactFromAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["username"]
        amount = serializer.validated_data["amount"]
        transact_from_admin(user, amount)
        return Response({"amount": user.money})


class TransactToAdminView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TransactToAdminSerializer)
    def post(self, request):
        serializer = TransactToAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        transact_to_admin(request.user, amount)
        return Response({"amount": request.user.money})


class TransactToUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TransactFromAdminSerializer)
    def post(self, request):
        serializer = TransactFromAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["username"]
        amount = serializer.validated_data["amount"]
        t = Transaction.objects.create(
            user_from=request.user, user_to=user, amount=amount
        )
        return Response({"your_amount": t.user_from.money, "amount": t.user_to.money})


class GetMoneyApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_money = int(get_balance(request.user.wallet_public_key).coins)
        if request.user.money != user_money:
            request.user.money = user_money
            request.user.save(update_fields=["money"])

        return Response({"amount": user_money})


class TransactionHistoryApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(list_user_transactions(request.user))
