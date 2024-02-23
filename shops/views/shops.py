from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopRetrieveUpdateApi', 'ShopGiftPhotoUpdateApi')


class ShopGiftPhotoUpdateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        gift_photo = serializers.ImageField()

    def post(self, request: Request) -> Response:
        bot: Bot = request.META['bot']
        photo: InMemoryUploadedFile | None = request.data.get('photo')

        if photo is None:
            raise ValidationError({'photo': 'This field is required'})

        shop = bot.shop

        shop.gift_photo = photo
        shop.save()

        serializer = self.OutputSerializer(shop)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class ShopRetrieveUpdateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputUpdateSerializer(serializers.Serializer):
        gift_name = serializers.CharField(max_length=64)
        start_text = serializers.CharField(max_length=4096)
        each_nth_cup_free = serializers.IntegerField()
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
        shop.gift_name = serialized_data['gift_name']
        shop.each_nth_sale_free = serialized_data['each_nth_cup_free']
        shop.start_text = serialized_data['start_text']
        shop.is_menu_shown = serialized_data['is_menu_shown']
        shop.save()

        response_data = {'ok': True, 'result': self.OutputSerializer(shop).data}
        return Response(response_data)
