from dataclasses import dataclass

from django.db import models

from shops.models.shop_groups import ShopGroup
from telegram.models.users import User

__all__ = ('ShopClient', 'ShopClientStatistics')


@dataclass(frozen=True, slots=True)
class ShopClientStatistics:
    user_id: int
    has_gift: bool
    shop_group_bot_id: int
    each_nth_cup_free: int
    purchases_count: int
    current_cups_count: int


class ShopClient(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )
    shop_group = models.ForeignKey(
        to=ShopGroup,
        on_delete=models.CASCADE,
    )
    has_gift = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        unique_together = ('user', 'shop_group')

    def __str__(self) -> str:
        return str(self.user)
