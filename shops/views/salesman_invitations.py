from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import (
    get_shop_admin,
    get_shop_group_by_bot_id
)
from shops.services.salesman_invitations import create_salesman_invitation

__all__ = ('SalesmanInvitationCreateApi',)


class SalesmanInvitationCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        admin_user_id = serializers.IntegerField()
        bot_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        created_at = serializers.DateTimeField()
        expires_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        admin_user_id: int = serialized_data['admin_user_id']
        bot_id: int = serialized_data['bot_id']

        shop_group = get_shop_group_by_bot_id(bot_id)

        shop_admin = get_shop_admin(
            user_id=admin_user_id,
            shop_group_id=shop_group.id,
        )
        salesman_invitation = create_salesman_invitation(shop_admin)

        serializer = self.OutputSerializer(salesman_invitation)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
