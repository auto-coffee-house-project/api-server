import json

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mailing.serializers import ButtonSerializer, SegregationOptionsSerializer
from mailing.tasks import start_mailing_task
from shops.permissions import HasShop
from telegram.authentication import BotAuthentication
from telegram.models import Bot, Button
from telegram.permissions import HasBot

__all__ = ('MailingCreateApi',)


class MailingCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField(max_length=4096)
        buttons = ButtonSerializer(many=True, default=list)
        parse_mode = serializers.ChoiceField(
            choices=['HTML', 'MarkdownV2'],
            allow_null=True,
            default=None,
        )
        photo = Base64ImageField(
            represent_in_base64=True,
            allow_null=True,
            default=None,
        )
        segregation_options = SegregationOptionsSerializer(
            default=dict,
            required=False,
        )

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        text: str = serialized_data['text']
        buttons: list[Button] = serialized_data['buttons']
        parse_mode: str | None = serialized_data['parse_mode']
        base64_photo: str | None = serialized_data['photo']
        segregation_options: dict = serialized_data['segregation_options']

        start_mailing_task.delay(
            shop_id=bot.shop.id,
            text=text,
            buttons_json=json.dumps(buttons),
            parse_mode=parse_mode,
            base64_photo=base64_photo,
            segregation_options_json=json.dumps(
                segregation_options,
                default=str,
            ),
        )

        return Response({'ok': True}, status=status.HTTP_202_ACCEPTED)
