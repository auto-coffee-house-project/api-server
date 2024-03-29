from decimal import Decimal

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.services.shop_products import create_shop_product
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopProductListCreateApi',)


class ShopProductListCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot]

    class InputSerializer(serializers.Serializer):
        class PhotoSerializer(serializers.Serializer):
            url = serializers.URLField()
            is_main = serializers.BooleanField()

        name = serializers.CharField(max_length=100)
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        category_ids = serializers.ListField(child=serializers.IntegerField())
        photos = PhotoSerializer(many=True)

    class OutputSerializer(serializers.Serializer):
        class CategorySerializer(serializers.Serializer):
            id = serializers.IntegerField()
            name = serializers.CharField()

        class PhotoSerializer(serializers.Serializer):
            url = serializers.URLField()
            is_main = serializers.BooleanField()

        id = serializers.IntegerField()
        name = serializers.CharField()
        price = serializers.DecimalField()
        categories = CategorySerializer(many=True)
        photos = PhotoSerializer(many=True)

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        name: str = serialized_data['name']
        price: Decimal = serialized_data['price']
        category_ids: set[int] = set(serialized_data['category_ids'])
        photos: list[dict[str, any]] = serialized_data['photos']

        bot: Bot = request.META['bot']

        product = create_shop_product(
            name=name,
            price=price,
            shop_group=bot.shopgroup,
            category_ids=category_ids,
            photos=photos,
        )

        serializer = self.OutputSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
