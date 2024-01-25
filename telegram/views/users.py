from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram.models import User
from telegram.selectors import get_user_role
from telegram.services.users import upsert_user

__all__ = ('UserCreateUpdateApi', 'UserRetrieveApi')


class UserRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        username = serializers.CharField()
        created_at = serializers.DateTimeField()

    def get(self, request: Request, user_id: int):
        user = User.objects.get(id=user_id)
        role = get_user_role(user.id)
        serializer = self.OutputSerializer(user)
        response_data = {'ok': True, 'result': serializer.data | {'role': role}}
        return Response(response_data)


class UserCreateUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(allow_null=True)
        username = serializers.CharField(allow_null=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        username = serializers.CharField()
        created_at = serializers.DateTimeField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user, is_created = upsert_user(
            id_=serialized_data['id'],
            first_name=serialized_data['first_name'],
            last_name=serialized_data['last_name'],
            username=serialized_data['username'],
        )
        role = get_user_role(user.id)

        serializer = self.OutputSerializer(user)
        status_code = (
            status.HTTP_201_CREATED if is_created
            else status.HTTP_200_OK
        )
        response_data = {'ok': True, 'result': serializer.data | {'role': role}}
        return Response(response_data, status=status_code)
