import random
import string
from datetime import datetime, timedelta
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

from shops.models.shop_clients import ShopClient
from shops.models.shops import Shop


def generate_code() -> str:
    return ''.join(random.choices(string.digits, k=4))


class GiftCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    client = models.ForeignKey(to=ShopClient, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, default=generate_code)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'gift code'
        verbose_name_plural = 'gift codes'
        unique_together = ('shop', 'code')

    def __str__(self):
        return self.code

    @property
    def expires_at(self) -> datetime:
        return self.created_at + timedelta(
            seconds=settings.GIFT_CODE_LIFETIME_SECONDS,
        )

    @property
    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()
