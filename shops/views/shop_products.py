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

    class InputCreateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        category_ids = serializers.ListField(
            child=serializers.IntegerField(),
            required=False,
            allow_empty=True,
        )

    class OutputSerializer(serializers.Serializer):
        class CategorySerializer(serializers.Serializer):
            id = serializers.IntegerField()
            name = serializers.CharField()

        id = serializers.IntegerField()
        name = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        categories = CategorySerializer(many=True)
        photo = serializers.ImageField(allow_null=True)

    def get(self, request: Request) -> Response:
        bot: Bot = request.META['bot']

        products = bot.shopgroup.shopproduct_set.order_by('-created_at')

        serializer = self.OutputSerializer(products, many=True)
        response_data = {
            'ok': True,
            'result': serializer.data,
        }
        return Response(response_data)

    def post(self, request: Request) -> Response:
        serializer = self.InputCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        name: str = serialized_data['name']
        price: Decimal = serialized_data['price']
        category_ids: set[int] = set(serialized_data['category_ids'])

        bot: Bot = request.META['bot']

        product = create_shop_product(
            name=name,
            price=price,
            shop_group_id=bot.shopgroup.id,
            category_ids=category_ids,
        )

        serializer = self.OutputSerializer(product)
        response_data = {
            'ok': True,
            'result': serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
