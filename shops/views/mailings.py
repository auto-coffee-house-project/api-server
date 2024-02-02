from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_group_by_bot_id
from shops.tasks import start_mailing


class MailingCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField()
        admin_user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        admin_user_id = serialized_data['admin_user_id']
        text = serialized_data['text']
        bot_id = serialized_data['bot_id']

        shop_group = get_shop_group_by_bot_id(bot_id)

        start_mailing.delay(admin_user_id, shop_group.id, text)

        response_data = {'ok': True}
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
