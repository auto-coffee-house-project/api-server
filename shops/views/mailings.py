import json

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.tasks import start_mailing
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot


class MailingCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):

        class ButtonSerializer(serializers.Serializer):
            text = serializers.CharField(max_length=64)
            url = serializers.URLField()

        text = serializers.CharField(max_length=4096)
        buttons = ButtonSerializer(many=True)
        is_markdown = serializers.BooleanField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        text = serialized_data['text']
        buttons = serialized_data['buttons']
        is_markdown = serialized_data['is_markdown']

        parse_mode = 'Markdown' if is_markdown else None

        start_mailing.delay(
            bot.shop.id,
            text,
            parse_mode,
            json.dumps(buttons, ensure_ascii=False),
        )

        response_data = {'ok': True}
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
