from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram.services.users import upsert_user

__all__ = ('UserCreateUpdateApi',)


class UserCreateUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        username = serializers.CharField()

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

        serializer = self.OutputSerializer(user)
        status_code = (
            status.HTTP_201_CREATED if is_created
            else status.HTTP_200_OK
        )
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data, status=status_code)
