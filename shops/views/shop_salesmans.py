from uuid import UUID

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import (
    get_salesman_invitation_by_id,
    get_shop_group_by_bot_id,
    get_shop_admin,
    get_shop_salesman,
)
from shops.services.shop_salesmans import create_salesman_by_invitation

__all__ = ('ShopSalesmanListCreateDeleteApi',)


class ShopSalesmanListCreateDeleteApi(APIView):

    class InputListSerializer(serializers.Serializer):
        admin_user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

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

    class InputDeleteSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        serializer = self.InputListSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        admin_user_id: int = serialized_data['admin_user_id']
        bot_id: int = serialized_data['bot_id']

        shop_group = get_shop_group_by_bot_id(bot_id)
        shop_admin = get_shop_admin(
            user_id=admin_user_id,
            shop_group_id=shop_group.id,
        )

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

    def delete(self, request: Request) -> Response:
        serializer = self.InputDeleteSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        bot_id: int = serialized_data['bot_id']

        shop_group = get_shop_group_by_bot_id(bot_id)
        shop_salesman = get_shop_salesman(
            user_id=user_id,
            shop_group_id=shop_group.id,
        )
        shop_salesman.delete()

        response_data = {'ok': True}
        return Response(response_data)
