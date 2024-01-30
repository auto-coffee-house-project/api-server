from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram.selectors import get_bots, get_bot_by_id

__all__ = ('BotListApi', 'BotRetrieveApi')


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


class BotRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        token = serializers.CharField()
        username = serializers.CharField()
        start_text = serializers.CharField()
        created_at = serializers.DateTimeField()

    def get(self, request: Request, bot_id: int) -> Response:
        bot = get_bot_by_id(bot_id)
        serializer = self.OutputSerializer(bot)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
