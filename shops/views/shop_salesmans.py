from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_salesman_by_user_id

__all__ = ('ShopSalesmanRetrieveApi',)


class ShopSalesmanRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user_id = serializers.IntegerField()

    def get(self, request: Request, user_id: int) -> Response:
        salesman = get_shop_salesman_by_user_id(user_id)
        serializer = self.OutputSerializer(salesman)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
