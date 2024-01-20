from rest_framework.generics import CreateAPIView, RetrieveAPIView

from telegram.models import User
from telegram.serializers import UserSerializer

__all__ = (
    'UserCreateApi',
    'UserRetrieveApi',
)


class UserCreateApi(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveApi(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
