import random
import string
from uuid import uuid4

from django.db import models

from shops.models.shop_clients import ShopClient
from shops.models.shops import Shop

__all__ = ('Gift',)


def generate_code() -> str:
    return random.choices(string.digits, k=4)


class Gift(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    code = models.CharField(max_length=4, db_index=True, default=generate_code)
    client = models.ForeignKey(
        to=ShopClient,
        on_delete=models.CASCADE,
    )
    shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'gifts'
        unique_together = ('shop', 'code')
