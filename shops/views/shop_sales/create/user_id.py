from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import (
    get_shop_client_by_user_id,
    get_shop_salesman,
    get_shop_group_by_bot_id,
)
from shops.services.shop_clients import get_shop_client_statistics
from shops.services.shop_sales import create_shop_sale_by_user_id

__all__ = ('ShopSaleCreateByUserIdApi',)


class ShopSaleCreateByUserIdApi(APIView):

    class InputSerializer(serializers.Serializer):
        client_user_id = serializers.IntegerField()
        salesman_user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        is_free = serializers.BooleanField()
        client_user_id = serializers.IntegerField(source='client.user_id')

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        client_user_id: int = serialized_data['client_user_id']
        salesman_user_id: int = serialized_data['salesman_user_id']
        bot_id: int = serialized_data['bot_id']

        shop_group = get_shop_group_by_bot_id(bot_id)

        shop_client = get_shop_client_by_user_id(client_user_id, bot_id)
        shop_salesman = get_shop_salesman(
            user_id=salesman_user_id,
            shop_group_id=shop_group.id,
        )

        shop_sale = create_shop_sale_by_user_id(
            shop_client=shop_client,
            shop_salesman=shop_salesman,
        )
        shop_client_statistics = get_shop_client_statistics(
            shop_client=shop_client,
            shop_group=shop_salesman.shop.group,
        )

        serializer = self.OutputSerializer(shop_sale)

        response_data = {
            'ok': True,
            'result': serializer.data | {
                'shop_group_bot_id': shop_client_statistics.shop_group_bot_id,
                'each_nth_cup_free': shop_client_statistics.each_nth_cup_free,
                'purchases_count': shop_client_statistics.purchases_count,
                'current_cups_count': shop_client_statistics.current_cups_count,
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
