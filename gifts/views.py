from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from gifts.serializers import GiftSerializer
from gifts.services import GiftCreateContext, activate_gift
from shops.permissions import HasShop
from shops.selectors import get_shop_client
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('GiftListCreateApi', 'GiftActivateApi')


class GiftActivateApi(APIView):
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

        activate_gift(
            shop_id=bot.shop.id,
            code=code,
            employee_user_id=employee_user_id,
        )
        return Response({'ok': True})


class GiftListCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    OutputCreateSerializer = GiftSerializer

    def get(self, request: Request, client_user_id: int) -> Response:
        bot: Bot = request.META['bot']

        client = get_shop_client(user_id=client_user_id, shop_id=bot.shop.id)
        gifts = client.gift_set.all()

        serializer = GiftSerializer(gifts, many=True)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def post(self, request: Request, client_user_id: int) -> Response:
        bot: Bot = request.META['bot']

        client = get_shop_client(user_id=client_user_id, shop_id=bot.shop.id)

        gift_context = GiftCreateContext(
            client=client,
            shop=bot.shop,
        )
        gift = gift_context.create_extra_gift()

        serializer = self.OutputCreateSerializer(gift)
        return Response(
            {'ok': True, 'result': serializer.data},
            status=status.HTTP_201_CREATED,
        )
