from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.selectors import get_shop_client, get_shop_employee
from shops.services.shop_clients import get_shop_client_statistics
from shops.services.shop_sales import create_shop_sale_by_user_id
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopSaleCreateByUserIdApi',)


class ShopSaleCreateByUserIdApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class InputSerializer(serializers.Serializer):
        client_user_id = serializers.IntegerField()
        employee_user_id = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        shop = bot.shop

        client_user_id: int = serialized_data['client_user_id']
        employee_user_id: int = serialized_data['employee_user_id']

        client = get_shop_client(user_id=client_user_id, shop_id=shop.id)
        employee = get_shop_employee(user_id=employee_user_id, shop_id=shop.id)

        sale = create_shop_sale_by_user_id(client=client, employee=employee)
        client_statistics = get_shop_client_statistics(client)

        response_data = {
            'ok': True,
            'result': {
                'id': sale.id,
                'is_free': sale.is_free,
                'client_id': sale.client_id,
                'client_user_id': sale.client.user_id,
                'total_purchases_count': client_statistics.total_purchases_count,
                'current_cups_count': client_statistics.current_cups_count,
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
