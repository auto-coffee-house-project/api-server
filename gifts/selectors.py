from django.db.models import QuerySet
from django.utils import timezone

from gifts.models import Gift

__all__ = ('get_expired_gifts',)


def get_expired_gifts() -> QuerySet[Gift]:
    return Gift.objects.filter(expires_at__lt=timezone.now())
