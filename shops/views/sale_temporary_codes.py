from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_client_by_user_id, get_shop_group_by_bot_id
from shops.services.sale_temporary_codes import create_sale_temporary_code

__all__ = ('SaleTemporaryCodeCreateApi',)


class SaleTemporaryCodeCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        bot_id = serializers.IntegerField()
        client_user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        code = serializers.CharField()
        created_at = serializers.DateTimeField()
        expires_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serialized_data = serializer.data

        client_user_id: int = serialized_data['client_user_id']
        bot_id: int = serialized_data['bot_id']

        shop_client = get_shop_client_by_user_id(client_user_id)
        shop_group = get_shop_group_by_bot_id(bot_id)

        sale_temporary_code = create_sale_temporary_code(
            shop_client_id=shop_client.id,
            shop_group_id=shop_group.id,
        )

        serializer = self.OutputSerializer(sale_temporary_code)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
