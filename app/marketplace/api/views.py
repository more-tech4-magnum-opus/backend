from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from blockchain.services import transact_to_admin
from conf import settings
from marketplace.api.serializers import ProductSerializer
from marketplace.models import Product
from common.permissions import IsManager
from utils.blockchain import transfer_nft


class ListCreateProductApi(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Product.objects.all()


class RetrieveUpdateDestroyProductApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Product.objects.all()

    def get_object(self):
        product = get_object_or_404(
            Product,
            slug=self.request.parser_context["kwargs"]["slug"],
        )
        return product


class BuyProductApi(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        product = get_object_or_404(
            Product,
            slug=self.request.parser_context["kwargs"]["slug"],
        )
        transact_to_admin(self.request.user, product.price)
        transfer_nft(settings.MAIN_WALLET, self.request.user.wallet_public_key, product.token)
        return product
