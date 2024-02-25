from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot
from telegram.selectors import get_bots

__all__ = ('BotListApi', 'BotRetrieveUpdateApi')


class BotListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        token = serializers.CharField()
        username = serializers.CharField()
        start_text = serializers.CharField()
        created_at = serializers.DateTimeField()

    def get(self, request: Request) -> Response:
        bots = get_bots()
        serializer = self.OutputSerializer(bots, many=True)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class BotRetrieveUpdateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot]

    class InputUpdateSerializer(serializers.Serializer):
        start_text = serializers.CharField(max_length=1024)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        token = serializers.CharField()
        username = serializers.CharField()
        start_text = serializers.CharField()
        created_at = serializers.DateTimeField()

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

        bot.start_text = serialized_data['start_text']
        bot.save()

        serializer = self.OutputSerializer(bot)

        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
