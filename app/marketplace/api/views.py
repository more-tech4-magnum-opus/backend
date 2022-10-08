from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser

from marketplace.api.serializers import ProductSerializer
from marketplace.models import Product
from common.permissions import IsManager


class ListCreateProductApi(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Product.objects.all()


class RetireUpdateDestroyProductApi(generics.RetrieveUpdateDestroyAPIView):
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
