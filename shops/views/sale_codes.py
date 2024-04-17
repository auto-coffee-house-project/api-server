from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.selectors import get_shop_client
from shops.services.sale_codes import refresh_sale_code
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('SaleCodeCreateApi',)


class SaleCodeCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):
        client_user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        client_id = serializers.IntegerField(source='client.id')
        client_user_id = serializers.IntegerField(source='client.user.id')
        code = serializers.CharField()
        created_at = serializers.DateTimeField()
        expires_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        client_user_id: int = serialized_data['client_user_id']
        bot: Bot = request.META['bot']

        shop = bot.shop

        client = get_shop_client(user_id=client_user_id, shop_id=shop.id)
        sale_code = refresh_sale_code(client_id=client.id, shop_id=shop.id)

        serializer = self.OutputSerializer(sale_code)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
