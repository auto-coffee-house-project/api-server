from django.db import models

from shops.models.shop_products import ShopProduct

__all__ = ('ShopProductPhoto',)


class ShopProductPhoto(models.Model):
    product = models.ForeignKey(
        to=ShopProduct,
        on_delete=models.CASCADE,
    )
    url = models.URLField()
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
