from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.selectors import get_sale_code, get_shop_employee
from shops.services.shop_clients import get_shop_client_statistics
from shops.services.shop_sales import create_shop_sale_by_code
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopSaleCreateByCodeApi',)


class ShopSaleCreateByCodeApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        employee_user_id = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        shop = bot.shop

        code: str = serialized_data['code']
        employee_user_id: int = serialized_data['employee_user_id']

        sale_code = get_sale_code(shop_id=shop.id, code=code)
        employee = get_shop_employee(user_id=employee_user_id, shop_id=shop.id)
        sale = create_shop_sale_by_code(
            employee=employee,
            sale_code=sale_code,
        )

        shop_client_statistics = get_shop_client_statistics(sale_code.client)

        response_data = {
            'ok': True,
            'result': {
                'id': sale.id,
                'is_free': sale.is_free,
                'client_id': sale.client_id,
                'client_user_id': sale.client.user_id,
                'total_purchases_count': shop_client_statistics.total_purchases_count,
                'current_cups_count': shop_client_statistics.current_cups_count,
            },
        }
        return Response(response_data)
