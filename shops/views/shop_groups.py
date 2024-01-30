from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_group_by_bot_id

__all__ = ('ShopGroupRetrieveApi',)


class ShopGroupRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        each_nth_cup_free = serializers.IntegerField()
        created_at = serializers.DateTimeField()

    def get(self, request: Request, bot_id: int) -> Response:
        shop_group = get_shop_group_by_bot_id(bot_id)
        serializer = self.OutputSerializer(shop_group)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
