from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_group_by_bot_id
from shops.services.shop_clients import get_or_create_shop_client
from telegram.selectors import get_user_role, get_user_by_id
from telegram.services.users import upsert_user

__all__ = ('UserRetrieveCreateUpdateApi',)


class UserRetrieveCreateUpdateApi(APIView):

    class InputRetrieveSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    class InputCreateUpdateSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(allow_null=True)
        username = serializers.CharField(allow_null=True)
        bot_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(allow_null=True)
        username = serializers.CharField(allow_null=True)
        created_at = serializers.DateTimeField()

    def get(self, request: Request) -> Response:
        serializer = self.InputRetrieveSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        bot_id: int = serialized_data['bot_id']

        shop_group = get_shop_group_by_bot_id(bot_id)

        user = get_user_by_id(user_id)
        role = get_user_role(user_id=user_id, shop_group_id=shop_group.id)

        serializer = self.OutputSerializer(user)
        response_data = {
            'ok': True,
            'result': serializer.data | {'role': role},
        }
        return Response(response_data)

    def post(self, request: Request):
        serializer = self.InputCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot_id: int = serialized_data['bot_id']

        shop_group = get_shop_group_by_bot_id(bot_id)

        user, is_created = upsert_user(
            id_=serialized_data['id'],
            first_name=serialized_data['first_name'],
            last_name=serialized_data['last_name'],
            username=serialized_data['username'],
        )
        get_or_create_shop_client(user.id)
        role = get_user_role(user_id=user.id, shop_group_id=shop_group.id)

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
