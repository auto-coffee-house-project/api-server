from dataclasses import dataclass

from django.db import models

from shops.models.shops import Shop

__all__ = ('ShopClient', 'ClientUser', 'ShopClientStatistics')

from telegram.models import User


@dataclass(frozen=True, slots=True)
class ClientUser:
    id: int
    first_name: str
    last_name: str
    username: str


@dataclass(frozen=True, slots=True)
class ShopClientStatistics:
    client_id: int
    user: ClientUser
    has_gift: bool
    total_purchases_count: int
    free_purchases_count: int
    current_cups_count: int


class ShopClient(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    has_gift = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        unique_together = ('user', 'shop')

    def __str__(self) -> str:
        return str(self.user)
