from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.tasks import start_mailing
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot


class MailingCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot]

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField()
        admin_user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        admin_user_id = serialized_data['admin_user_id']
        text = serialized_data['text']

        start_mailing.delay(admin_user_id, bot.shop.id, text)

        response_data = {'ok': True}
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
