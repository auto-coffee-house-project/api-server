from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import (
    get_shop_client_by_user_id,
    get_shop_admin_by_user_id,
    count_client_purchases_in_shop_group, get_shop_group_by_bot_id,
)

__all__ = ('ShopClientStatisticsRetrieveApi',)


class ShopClientStatisticsRetrieveApi(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        bot_id: int = serialized_data['bot_id']

        shop_client = get_shop_client_by_user_id(user_id)
        shop_group = get_shop_group_by_bot_id(bot_id)

        purchases_count = count_client_purchases_in_shop_group(
            client_id=shop_client.id,
            shop_group_id=shop_group.id,
        )
        current_cups_count = purchases_count % shop_group.each_nth_cup_free

        response_data = {
            'ok': True,
            'result': {
                'user_id': shop_client.user.id,
                'purchases_count': purchases_count,
                'each_nth_cup_free': shop_group.each_nth_cup_free,
                'current_cups_count': current_cups_count,
            },
        }
        return Response(response_data)
