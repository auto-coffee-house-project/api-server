import json

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mailing.tasks import create_mailing
from shops.permissions import HasShop
from telegram.authentication import BotAuthentication
from telegram.models import Bot, Button
from telegram.permissions import HasBot

__all__ = ('MailingCreateApi',)


class MailingCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):
        class ButtonSerializer(serializers.Serializer):
            text = serializers.CharField(max_length=64)
            url = serializers.URLField()

        text = serializers.CharField(max_length=4096)
        buttons = ButtonSerializer(many=True)
        parse_mode = serializers.ChoiceField(
            choices=['HTML', 'Markdown'],
            allow_null=True,
            default=None,
        )
        photo = Base64ImageField(
            represent_in_base64=True,
            allow_null=True,
            default=None,
        )

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        text: str = serialized_data['text']
        buttons: list[Button] = serialized_data['buttons']
        parse_mode: str = serialized_data['parse_mode']
        base64_photo: str | None = serialized_data['photo']

        create_mailing.delay(
            shop_id=bot.shop.id,
            text=text,
            buttons_json=json.dumps(buttons),
            parse_mode=parse_mode,
            base64_photo=base64_photo,
        )

        return Response({'ok': True}, status=status.HTTP_202_ACCEPTED)
