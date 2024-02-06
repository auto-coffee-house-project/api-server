from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_group_by_bot_id

__all__ = ('ShopGroupRetrieveUpdateApi',)


class ShopGroupRetrieveUpdateApi(APIView):
    class InputUpdateSerializer(serializers.Serializer):
        gift_name = serializers.CharField(max_length=64)
        gift_photo_url = serializers.URLField(allow_null=True)
        each_nth_cup_free = serializers.IntegerField()
        is_menu_shown = serializers.BooleanField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        gift_name = serializers.CharField()
        gift_photo_url = serializers.URLField(allow_null=True)
        each_nth_cup_free = serializers.IntegerField()
        is_menu_shown = serializers.BooleanField()
        created_at = serializers.DateTimeField()

    def get(self, request: Request, bot_id: int) -> Response:
        shop_group = get_shop_group_by_bot_id(bot_id)
        serializer = self.OutputSerializer(shop_group)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def put(self, request: Request, bot_id: int) -> Response:
        serializer = self.InputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        shop_group = get_shop_group_by_bot_id(bot_id)

        shop_group.gift_name = serialized_data['gift_name']
        shop_group.gift_photo_url = serialized_data['gift_photo_url']
        shop_group.each_nth_cup_free = serialized_data['each_nth_cup_free']
        shop_group.is_menu_shown = serialized_data['is_menu_shown']
        shop_group.save()

        response_data = {'ok': True, 'result': self.OutputSerializer(shop_group).data}
        return Response(response_data)
