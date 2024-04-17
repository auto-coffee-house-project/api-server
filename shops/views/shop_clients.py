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

        class GiftSerializer(serializers.Serializer):
            code = serializers.CharField()
            is_main = serializers.BooleanField()
            expires_at = serializers.DateTimeField()

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
        gifts = GiftSerializer(many=True)
        born_on = serializers.DateField()

    class InputUpdateSerializer(serializers.Serializer):
        born_on = serializers.DateField(required=False, allow_null=True)
        has_gift = serializers.BooleanField(required=False)

    def get(self, request: Request, user_id: int) -> Response:
        bot: Bot = request.META['bot']

        shop_client = get_shop_client(user_id=user_id, shop_id=bot.shop.id)

        shop_client_statistics = get_shop_client_statistics(shop_client)

        serializer = self.OutputSerializer(shop_client_statistics)

        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def patch(self, request: Request, user_id: int) -> Response:
        serializer = self.InputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        client = get_shop_client(user_id=user_id, shop_id=bot.shop.id)

        if 'born_on' in serialized_data:
            client.born_on = serialized_data['born_on']

        if 'has_gift' in serialized_data:
            client.has_gift = serialized_data['has_gift']

        client.save()

        client_statistics = get_shop_client_statistics(client)

        serializer = self.OutputSerializer(client_statistics)
        response_data = {
            'ok': True,
            'result': serializer.data,
        }
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
        born_on = serializers.DateField()

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
