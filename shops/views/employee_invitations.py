from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.selectors import get_shop_employee
from shops.services.employee_invitations import (
    build_invitation_url,
    create_employee_invitation,
)
from telegram.authentication import BotAuthentication
from telegram.models import Bot
from telegram.permissions import HasBot

__all__ = ('EmployeeInvitationCreateApi',)


class EmployeeInvitationCreateApi(APIView):
    authentication_classes = [BotAuthentication]
    permission_classes = [HasBot]

    class InputSerializer(serializers.Serializer):
        admin_user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        created_at = serializers.DateTimeField()
        expires_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        bot: Bot = request.META['bot']

        admin_user_id: int = serialized_data['admin_user_id']

        employee = get_shop_employee(
            user_id=admin_user_id,
            shop_id=bot.shop.id,
        )
        employee_invitation = create_employee_invitation(employee)

        invitation_url = build_invitation_url(
            bot_username=bot.username,
            invitation_id=employee_invitation.id,
        )

        serializer = self.OutputSerializer(employee_invitation)
        response_data = {
            'ok': True,
            'result': serializer.data | {'url': invitation_url},
        }
        return Response(response_data)
