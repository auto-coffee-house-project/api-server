from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot
from telegram.selectors import get_bots

__all__ = ('BotListApi', 'BotRetrieveUpdateApi')

from telegram.services.bots import update_bot


class BotListApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Bot
            fields = (
                'id',
                'name',
                'token',
                'username',
                'start_text',
                'sale_created_text',
                'gift_given_text',
                'created_at',
            )

    def get(self, request: Request) -> Response:
        bots = get_bots()
        serializer = self.OutputSerializer(bots, many=True)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class BotRetrieveUpdateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot]

    class InputUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Bot
            fields = ('start_text', 'sale_created_text', 'gift_given_text')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Bot
            fields = (
                'id',
                'name',
                'token',
                'username',
                'start_text',
                'sale_created_text',
                'gift_given_text',
                'created_at',
            )

    def get(self, request: Request) -> Response:
        bot: Bot = request.META['bot']
        serializer = self.OutputSerializer(bot)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def put(self, request) -> Response:
        serializer = self.InputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        update_bot(
            bot=bot,
            start_text=serialized_data['start_text'],
            sale_created_text=serialized_data['sale_created_text'],
            gift_given_text=serialized_data['gift_given_text'],
        )

        serializer = self.OutputSerializer(bot)

        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
