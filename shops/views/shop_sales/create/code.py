from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_sale_temporary_code, get_shop_salesman
from shops.services.shop_clients import get_shop_client_statistics
from shops.services.shop_sales import create_shop_sale_by_code

__all__ = ('ShopSaleCreateByCodeApi',)


class ShopSaleCreateByCodeApi(APIView):

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        salesman_user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        is_free = serializers.BooleanField()
        client_user_id = serializers.IntegerField(source='client.user_id')

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        code: str = serialized_data['code']
        salesman_user_id: int = serialized_data['salesman_user_id']

        sale_temporary_code = get_sale_temporary_code(code)
        salesman = get_shop_salesman(
            user_id=salesman_user_id,
            shop_group_id=sale_temporary_code.group_id,
        )
        shop_sale = create_shop_sale_by_code(
            salesman=salesman,
            sale_temporary_code=sale_temporary_code,
        )

        shop_client_statistics = get_shop_client_statistics(
            shop_client=sale_temporary_code.client,
            shop_group=sale_temporary_code.group,
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
        return Response(response_data)
