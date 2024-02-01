from uuid import UUID

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import (
    get_salesman_invitation_by_id,
    get_shop_admin_by_user_id,
)
from shops.services.shop_salesmans import create_salesman_by_invitation

__all__ = ('ShopSalesmanListCreateApi',)


class ShopSalesmanListCreateApi(APIView):

    class InputListSerializer(serializers.Serializer):
        admin_user_id = serializers.IntegerField()

    class OutputListSerializer(serializers.Serializer):
        class SalesmanSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            user_id = serializers.IntegerField(source='user.id')
            user_first_name = serializers.CharField(source='user.first_name')
            user_last_name = serializers.CharField(
                source='user.last_name',
                allow_null=True,
            )
            user_username = serializers.CharField(
                source='user.username',
                allow_null=True,
            )

        salesmans = SalesmanSerializer(
            many=True,
            source='shop.shopsalesman_set',
        )
        shop_name = serializers.CharField(source='shop.name')
        shop_group_name = serializers.CharField(source='shop.group.name')

    class InputCreateSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        invitation_id = serializers.UUIDField()

    class OutputCreateSerializer(serializers.Serializer):
        shop_name = serializers.CharField(source='shop.name')
        shop_group_name = serializers.CharField(source='shop.group.name')

    def get(self, request: Request) -> Response:
        serializer = self.InputListSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        admin_user_id: int = serialized_data['admin_user_id']

        shop_admin = get_shop_admin_by_user_id(admin_user_id)

        serializer = self.OutputListSerializer(shop_admin)

        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def post(self, request: Request) -> Response:
        serializer = self.InputCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        invitation_id: UUID = serialized_data['invitation_id']

        invitation = get_salesman_invitation_by_id(invitation_id)
        create_salesman_by_invitation(
            user_id=user_id,
            invitation=invitation,
        )

        serializer = self.OutputCreateSerializer(invitation)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
