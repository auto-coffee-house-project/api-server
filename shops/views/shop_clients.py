from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import (
    get_shop_client_by_user_id,
    get_shop_group_by_bot_id,
)
from shops.services.shop_clients import (
    get_shop_client_statistics,
    get_shop_client_statistics_list
)

__all__ = ('ShopClientStatisticsRetrieveApi', 'ShopClientStatisticsListApi')


class ShopClientStatisticsRetrieveApi(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        has_gift = serializers.BooleanField()
        shop_group_bot_id = serializers.IntegerField()
        each_nth_cup_free = serializers.IntegerField()
        purchases_count = serializers.IntegerField()
        current_cups_count = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        bot_id: int = serialized_data['bot_id']

        shop_client = get_shop_client_by_user_id(user_id)
        shop_group = get_shop_group_by_bot_id(bot_id)

        shop_client_statistics = get_shop_client_statistics(
            shop_client=shop_client,
            shop_group=shop_group,
        )

        serializer = self.OutputSerializer(shop_client_statistics)

        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class ShopClientStatisticsListApi(APIView):

    class InputSerializer(serializers.Serializer):
        bot_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        class UserSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            first_name = serializers.CharField()
            last_name = serializers.CharField(allow_null=True)
            username = serializers.CharField(allow_null=True)

        user = UserSerializer()
        shop_group_bot_id = serializers.IntegerField()
        each_nth_cup_free = serializers.IntegerField()
        purchases_count = serializers.IntegerField()
        current_cups_count = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot_id: int = serialized_data['bot_id']

        clients_statistics = get_shop_client_statistics_list(bot_id)

        response_data = {'ok': True, 'result': clients_statistics}
        return Response(response_data)
