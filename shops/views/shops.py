from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.services.shops import update_shop
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopRetrieveUpdateApi',)


class ShopRetrieveUpdateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputUpdateSerializer(serializers.Serializer):
        gift_name = serializers.CharField(max_length=64, required=False)
        gift_photo = Base64ImageField(
            represent_in_base64=True,
            required=False,
        )
        start_text = serializers.CharField(max_length=4096, required=False)
        each_nth_sale_free = serializers.IntegerField(required=False)
        is_menu_shown = serializers.BooleanField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        gift_name = serializers.CharField()
        gift_photo = serializers.ImageField(allow_null=True)
        start_text = serializers.CharField()
        each_nth_sale_free = serializers.IntegerField()
        is_menu_shown = serializers.BooleanField()
        created_at = serializers.DateTimeField()
        subscription_starts_at = serializers.DateTimeField()
        subscription_ends_at = serializers.DateTimeField()

    def get(self, request: Request) -> Response:
        bot: Bot = request.META['bot']
        serializer = self.OutputSerializer(bot.shop)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def patch(self, request: Request) -> Response:
        serializer = self.InputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        shop = update_shop(
            shop=bot.shop,
            fields=serialized_data,
            gift_photo_in_base64=request.data['gift_photo'],
        )
        serializer = self.OutputSerializer(shop)
        return Response({'ok': True, 'result': serializer.data})
