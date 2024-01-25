from uuid import UUID

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import (
    get_shop_salesman_by_user_id,
    get_salesman_invitation_by_id,
)
from shops.services.shop_salesmans import create_salesman_by_invitation

__all__ = (
    'ShopSalesmanRetrieveDeleteApi',
    'ShopSalesmanCreateApi',
)


class ShopSalesmanRetrieveDeleteApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user_id = serializers.IntegerField()

    def get(self, request: Request, user_id: int) -> Response:
        salesman = get_shop_salesman_by_user_id(user_id)
        serializer = self.OutputSerializer(salesman)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def delete(self, request: Request, user_id: int) -> Response:
        salesman = get_shop_salesman_by_user_id(user_id)
        salesman.delete()
        response_data = {'ok': True}
        return Response(response_data)


class ShopSalesmanCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        invitation_id = serializers.UUIDField()

    class OutputSerializer(serializers.Serializer):
        shop_name = serializers.CharField(source='shop.name')
        shop_group_name = serializers.CharField(source='shop.group.name')

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        invitation_id: UUID = serialized_data['invitation_id']

        invitation = get_salesman_invitation_by_id(invitation_id)
        create_salesman_by_invitation(
            user_id=user_id,
            invitation=invitation,
        )

        serializer = self.OutputSerializer(invitation)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
