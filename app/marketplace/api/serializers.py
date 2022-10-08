from rest_framework import serializers

from marketplace.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "image",
            "image_cropped",
            "nft",
            "price",
            "creator",
        ]
        extra_kwargs = {
            "image": {"write_only": True},
            "nft": {"read_only": True},
            "slug": {"read_only": True},
            "image_cropped": {"read_only": True},
            "creator": {"read_only": True},
        }

    def create(self, validated_data):
        return Product.objects.create(
            **validated_data, creator=self.context["request"].user
        )
