from rest_framework.generics import ListAPIView

from telegram.models import Bot
from telegram.serializers import BotSerializer

__all__ = ('BotListApi',)


class BotListApi(ListAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    pagination_class = None
