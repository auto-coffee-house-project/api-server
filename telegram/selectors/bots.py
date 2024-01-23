from django.db.models import QuerySet

from telegram.models import Bot

__all__ = ('get_bots',)


def get_bots() -> QuerySet[Bot]:
    return Bot.objects.order_by('created_at')
