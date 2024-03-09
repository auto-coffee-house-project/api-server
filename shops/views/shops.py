from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.services import base64_to_in_memory_uploaded_file
from shops.permissions import HasShop
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopRetrieveUpdateApi',)


class ShopRetrieveUpdateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputUpdateSerializer(serializers.Serializer):
        gift_name = serializers.CharField(max_length=64)
        gift_photo = Base64ImageField(
            allow_null=True,
            represent_in_base64=True,
            default=None,
        )
        start_text = serializers.CharField(max_length=4096)
        each_nth_sale_free = serializers.IntegerField()
        is_menu_shown = serializers.BooleanField()

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

    def put(self, request: Request) -> Response:
        serializer = self.InputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        shop = bot.shop

        # serialized_data['gift_photo'] does not contain content type
        gift_photo: str | None = request.data['gift_photo']

        if gift_photo is not None:
            shop.gift_photo = base64_to_in_memory_uploaded_file(
                base64_string=gift_photo,
                field_name='gift_photo',
            )

        shop.gift_name = serialized_data['gift_name']
        shop.each_nth_sale_free = serialized_data['each_nth_sale_free']
        shop.start_text = serialized_data['start_text']
        shop.is_menu_shown = serialized_data['is_menu_shown']
        shop.save()

        response_data = {'ok': True, 'result': self.OutputSerializer(shop).data}
        return Response(response_data)
