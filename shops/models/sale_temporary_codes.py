import random
import string
from datetime import timedelta, datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from shops.models.shop_clients import ShopClient
from shops.models.shop_groups import ShopGroup

__all__ = ('SaleTemporaryCode',)


def generate_code() -> str:
    return ''.join(random.choices(string.digits, k=4))


class SaleTemporaryCode(models.Model):
    client = models.ForeignKey(
        to=ShopClient,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        to=ShopGroup,
        on_delete=models.CASCADE,
    )
    code = models.CharField(max_length=4, default=generate_code)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'group', 'code')

    @property
    def expires_at(self) -> datetime:
        return self.created_at + timedelta(
            seconds=settings.SALE_TEMPORARY_CODE_LIFETIME_SECONDS,
        )

    @property
    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()
