from django.db.models import QuerySet

from core.exceptions import ObjectDoesNotExistError
from telegram.models import Bot

__all__ = ('get_bots', 'get_bot_by_id')


def get_bots() -> QuerySet[Bot]:
    return Bot.objects.order_by('created_at')


def get_bot_by_id(bot_id: int) -> Bot:
    try:
        return Bot.objects.get(id=bot_id)
    except Bot.DoesNotExist:
        raise ObjectDoesNotExistError({'bot_id': bot_id})
