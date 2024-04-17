from decimal import Decimal

from django.core.files.uploadedfile import InMemoryUploadedFile
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.services import base64_to_in_memory_uploaded_file
from shops.permissions import HasShop
from shops.selectors.shop_products import get_shop_product
from shops.services.shop_products import (
    create_shop_product,
    update_shop_product,
)
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = (
    'ShopProductListCreateApi',
    'ShopProductRetrieveUpdateDeleteApi',
)


class ShopProductRetrieveUpdateDeleteApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputUpdateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64)
        photo = Base64ImageField(
            represent_in_base64=True,
            allow_null=True,
            default=None,
        )
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        category_names = serializers.ManyRelatedField(
            child_relation=serializers.CharField(max_length=64),
            allow_empty=True,
            source='categories',
        )

    class OutputRetrieveUpdateSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        photo = serializers.ImageField(allow_null=True)
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        category_names = serializers.ManyRelatedField(
            child_relation=serializers.CharField(max_length=64),
            allow_empty=True,
            source='categories',
        )

    def get(self, request: Request, product_id: int) -> Response:
        bot: Bot = request.META['bot']
        shop_product = get_shop_product(
            shop_id=bot.shop.id,
            product_id=product_id,
        )

        serializer = self.OutputRetrieveUpdateSerializer(shop_product)
        response_data = {
            'ok': True,
            'result': serializer.data,
        }
        return Response(response_data)

    def put(self, request: Request, product_id: int) -> Response:
        serializer = self.InputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        # serialized_data['photo'] does not contain content type
        photo: str | None = request.data['photo']
        name: str = serialized_data['name']
        price: Decimal = serialized_data['price']
        category_names: set[str] = set(serialized_data['category_names'])

        if photo is not None:
            photo: InMemoryUploadedFile = base64_to_in_memory_uploaded_file(
                base64_string=photo,
            )

        bot: Bot = request.META['bot']
        product = get_shop_product(shop_id=bot.shop.id, product_id=product_id)

        product = update_shop_product(
            product=product,
            name=name,
            photo=photo,
            price=price,
            category_names=category_names,
        )

        serializer = self.OutputRetrieveUpdateSerializer(product)
        response_data = {
            'ok': True,
            'result': serializer.data,
        }
        return Response(response_data)

    def delete(self, request: Request, product_id: int) -> Response:
        bot: Bot = request.META['bot']
        shop_product = get_shop_product(
            shop_id=bot.shop.id,
            product_id=product_id,
        )
        shop_product.delete()
        return Response({'ok': True})


class ShopProductListCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot]

    class InputCreateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        category_names = serializers.ListField(
            child=serializers.CharField(max_length=64),
            allow_empty=True,
        )
        photo = Base64ImageField(
            represent_in_base64=True,
            allow_null=True,
            default=None,
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        category_names = serializers.ManyRelatedField(
            child_relation=serializers.CharField(max_length=64),
            allow_empty=True,
            source='categories',
        )
        photo = serializers.ImageField(allow_null=True)

    def get(self, request: Request) -> Response:
        bot: Bot = request.META['bot']

        products = bot.shop.shopproduct_set.order_by('-created_at')

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

        # serialized_data['photo'] does not contain content type
        photo: str | None = request.data['photo']

        if photo is not None:
            photo: InMemoryUploadedFile = base64_to_in_memory_uploaded_file(
                base64_string=photo,
            )

        name: str = serialized_data['name']
        price: Decimal = serialized_data['price']
        category_names: set[str] = set(serialized_data['category_names'])

        bot: Bot = request.META['bot']

        product = create_shop_product(
            name=name,
            photo=photo,
            price=price,
            shop_id=bot.shop.id,
            category_names=category_names,
        )

        serializer = self.OutputSerializer(product)
        response_data = {
            'ok': True,
            'result': serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
