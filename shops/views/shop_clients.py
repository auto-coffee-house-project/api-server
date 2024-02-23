from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.selectors import get_shop_client
from shops.services.shop_clients import (
    get_shop_client_statistics,
    get_shop_client_statistics_list,
)
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopClientRetrieveApi', 'ShopClientListApi')


class ShopClientRetrieveApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class OutputSerializer(serializers.Serializer):
        class UserSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            first_name = serializers.CharField()
            last_name = serializers.CharField(allow_null=True)
            username = serializers.CharField(allow_null=True)

        id = serializers.IntegerField(source='client_id')
        user = UserSerializer()
        total_purchases_count = serializers.IntegerField()
        free_purchases_count = serializers.IntegerField()
        current_cups_count = serializers.IntegerField()
        has_gift = serializers.BooleanField()

    def get(self, request: Request, user_id: int) -> Response:
        bot: Bot = request.META['bot']

        shop_client = get_shop_client(user_id=user_id, shop_id=bot.shop.id)

        shop_client_statistics = get_shop_client_statistics(
            shop_client=shop_client,
            shop=bot.shop,
        )

        serializer = self.OutputSerializer(shop_client_statistics)

        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class ShopClientListApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class OutputSerializer(serializers.Serializer):
        class UserSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            first_name = serializers.CharField()
            last_name = serializers.CharField(allow_null=True)
            username = serializers.CharField(allow_null=True)

        id = serializers.IntegerField(source='client_id')
        user = UserSerializer()
        total_purchases_count = serializers.IntegerField()
        free_purchases_count = serializers.IntegerField()
        current_cups_count = serializers.IntegerField()
        has_gift = serializers.BooleanField()

    def get(self, request: Request) -> Response:
        bot: Bot = request.META['bot']
        shop = bot.shop

        clients_statistics = get_shop_client_statistics_list(shop)

        serializer = self.OutputSerializer(clients_statistics, many=True)
        response_data = {
            'ok': True,
            'result': serializer.data,
        }
        return Response(response_data)
