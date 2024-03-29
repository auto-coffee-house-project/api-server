from django.db import models

from shops.models.shop_groups import ShopGroup

__all__ = ('Shop',)


class Shop(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(
        to=ShopGroup,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __str__(self) -> str:
        return self.name
