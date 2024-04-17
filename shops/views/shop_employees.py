from uuid import UUID

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.permissions import HasShop
from shops.selectors import get_employee_invitation, get_shop_employee_by_id
from shops.selectors.shop_employees import get_shop_employees
from shops.services.shop_employees import (
    create_employee_via_invitation,
    delete_shop_employee,
)
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('ShopEmployeeListCreateApi', 'ShopEmployeeDeleteApi')


class ShopEmployeeListCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    class OutputListSerializer(serializers.Serializer):
        class UserSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            first_name = serializers.CharField()
            last_name = serializers.CharField(allow_null=True)
            username = serializers.CharField(allow_null=True)

        id = serializers.IntegerField()
        user = UserSerializer()
        is_admin = serializers.BooleanField()

    class InputCreateSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        invitation_id = serializers.UUIDField()

    class OutputCreateSerializer(serializers.Serializer):
        class UserSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            first_name = serializers.CharField()
            last_name = serializers.CharField(allow_null=True)
            username = serializers.CharField(allow_null=True)

        id = serializers.IntegerField()
        shop_id = serializers.IntegerField(source='shop.id')
        shop_name = serializers.CharField(source='shop.name')
        user = UserSerializer()

    class InputDeleteSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        bot: Bot = request.META['bot']

        shop = bot.shop
        employees = get_shop_employees(bot.shop.id)

        serializer = self.OutputListSerializer(employees, many=True)
        response_data = {
            'ok': True,
            'result': {
                'shop_id': shop.id,
                'shop_name': shop.name,
                'employees': serializer.data,
            }
        }
        return Response(response_data)

    def post(self, request: Request) -> Response:
        serializer = self.InputCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        invitation_id: UUID = serialized_data['invitation_id']

        invitation = get_employee_invitation(invitation_id)
        employee = create_employee_via_invitation(
            user_id=user_id,
            invitation=invitation,
        )

        serializer = self.OutputCreateSerializer(employee)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class ShopEmployeeDeleteApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot, HasShop]

    def delete(self, request: Request, employee_id: int) -> Response:
        bot: Bot = request.META['bot']

        employee = get_shop_employee_by_id(employee_id)
        delete_shop_employee(employee=employee, shop=bot.shop)

        return Response({'ok': True})
