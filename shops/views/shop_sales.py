from django.db import transaction
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopSale
from shops.selectors import (
    get_sale_temporary_code,
    get_shop_salesman_by_user_id,
)
from shops.selectors.shop_sales import count_client_purchases_in_shop_group

__all__ = ('ShopSaleCreateApi', 'ShopSaleDeleteApi')


class ShopSaleCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        salesman_user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        is_free = serializers.BooleanField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        code: str = serialized_data['code']
        salesman_user_id: int = serialized_data['salesman_user_id']

        try:
            sale_temporary_code = get_sale_temporary_code(code)
        except ObjectDoesNotExistError as error:
            raise NotFound(error.message)

        try:
            salesman = get_shop_salesman_by_user_id(salesman_user_id)
        except ObjectDoesNotExistError as error:
            raise NotFound(error.message)

        if salesman.shop.group_id != sale_temporary_code.group_id:
            error = APIException(
                'Salesman does not belong to the same group as the code',
            )
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error

        if sale_temporary_code.is_expired:
            sale_temporary_code.delete()
            error = APIException('Code is expired')
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error

        sales_count = count_client_purchases_in_shop_group(
            client_id=sale_temporary_code.client_id,
            shop_group_id=salesman.shop.group_id,
        )

        is_free = sales_count % salesman.shop.group.each_nth_cup_free == 0

        with transaction.atomic():
            shop_sale = ShopSale.objects.create(
                shop=salesman.shop,
                client_id=sale_temporary_code.client_id,
                salesman=salesman,
                is_free=is_free,
            )
            sale_temporary_code.delete()

        serializer = self.OutputSerializer(shop_sale)
        return Response(serializer.data)


class ShopSaleDeleteApi(APIView):

    def delete(self, request: Request, shop_sale_id: int) -> Response:
        try:
            shop_sale = ShopSale.objects.get(id=shop_sale_id)
        except ShopSale.DoesNotExist:
            raise NotFound('Shop sale does not exist')
        shop_sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
