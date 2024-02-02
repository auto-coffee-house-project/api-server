from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_sale_by_id
from shops.services.shop_sales import delete_shop_sale

__all__ = ('ShopSaleDeleteApi',)


class ShopSaleDeleteApi(APIView):

    def delete(self, request: Request, sale_id: int) -> Response:
        shop_sale = get_shop_sale_by_id(sale_id)
        delete_shop_sale(shop_sale)
        response_data = {'ok': True}
        return Response(response_data)
