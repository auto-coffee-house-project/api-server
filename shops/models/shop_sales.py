from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from shops.models.shop_clients import ShopClient
from shops.models.shop_employee import ShopEmployee
from shops.models.shops import Shop

__all__ = ('ShopSale',)


class ShopSale(models.Model):
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    client = models.ForeignKey(to=ShopClient, on_delete=models.CASCADE)
    is_free = models.BooleanField(default=False)
    employee = models.ForeignKey(
        to=ShopEmployee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    comment = models.TextField(max_length=4096, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    @property
    def can_be_deleted_until(self) -> datetime:
        return self.created_at + timedelta(
            seconds=settings.SALE_CAN_BE_DELETED_IN_SECONDS,
        )
