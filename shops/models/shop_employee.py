from django.db import models

from shops.models.shops import Shop
from telegram.models.users import User

__all__ = ('ShopEmployee',)


class ShopEmployee(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'
        unique_together = ('user', 'shop')

    def __str__(self) -> str:
        return str(self.user)
