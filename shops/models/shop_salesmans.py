from django.db import models

from shops.models.shops import Shop
from telegram.models.users import User

__all__ = ('ShopSalesman',)


class ShopSalesman(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'salesman'
        verbose_name_plural = 'salesmans'
        unique_together = ('user', 'shop')

    def __str__(self) -> str:
        return str(self.user)
