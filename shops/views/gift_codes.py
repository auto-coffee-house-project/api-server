from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.selectors import get_shop_client
from shops.services.gift_codes import activate_gift_code, refresh_gift_code
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('GiftCodeCreateApi', 'GiftCodeActivateApi')


class GiftCodeCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):
        client_user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        client_id = serializers.IntegerField(source='client.id')
        client_user_id = serializers.IntegerField(source='client.user_id')
        code = serializers.CharField()
        created_at = serializers.DateTimeField()
        expires_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        client_user_id: int = serialized_data['client_user_id']
        bot: Bot = request.META['bot']

        client = get_shop_client(user_id=client_user_id, shop_id=bot.shop.id)
        gift_code = refresh_gift_code(client)

        serializer = self.OutputSerializer(gift_code)
        return Response(
            {'ok': True, 'result': serializer.data},
            status=status.HTTP_201_CREATED,
        )


class GiftCodeActivateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(max_length=4)
        employee_user_id = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']
        code: str = serialized_data['code']
        employee_user_id: int = serialized_data['employee_user_id']

        activate_gift_code(
            shop_id=bot.shop.id,
            code=code,
            employee_user_id=employee_user_id,
        )
        return Response({'ok': True})
