from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.tasks import start_mailing


class MailingCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField()
        admin_user_id = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        admin_user_id = serializer.validated_data['admin_user_id']
        text = serializer.validated_data['text']

        start_mailing.delay(admin_user_id, text)

        response_data = {'ok': True}
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
