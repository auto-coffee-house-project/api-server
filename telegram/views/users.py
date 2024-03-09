from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.services.shop_clients import get_or_create_shop_client
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot
from telegram.selectors import get_user_by_id, get_user_role
from telegram.services.users import upsert_user

__all__ = ('UserRetrieveApi', 'UserCreateUpdateApi')


class UserRetrieveApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(allow_null=True)
        username = serializers.CharField(allow_null=True)
        created_at = serializers.DateTimeField()

    def get(self, request: Request, user_id: int) -> Response:
        bot: Bot = request.META['bot']
        user = get_user_by_id(user_id)
        role = get_user_role(user_id=user_id, shop_id=bot.shop.id)

        serializer = self.OutputSerializer(user)
        response_data = {
            'ok': True,
            'result': serializer.data | {'role': role},
        }
        return Response(response_data)


class UserCreateUpdateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputCreateUpdateSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(allow_null=True)
        username = serializers.CharField(allow_null=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(allow_null=True)
        username = serializers.CharField(allow_null=True)
        created_at = serializers.DateTimeField()

    def post(self, request: Request):
        serializer = self.InputCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        user, is_created = upsert_user(
            id_=serialized_data['id'],
            first_name=serialized_data['first_name'],
            last_name=serialized_data['last_name'],
            username=serialized_data['username'],
        )
        get_or_create_shop_client(user_id=user.id, shop_id=bot.shop.id)
        role = get_user_role(user_id=user.id, shop_id=bot.shop.id)

        serializer = self.OutputSerializer(user)
        status_code = (
            status.HTTP_201_CREATED if is_created
            else status.HTTP_200_OK
        )
        response_data = {
            'ok': True,
            'result': serializer.data | {'role': role},
        }
        return Response(response_data, status=status_code)
