from django.db import models

from shops.models.shop_groups import ShopGroup
from shops.models.shop_product_categories import ShopProductCategory

__all__ = ('ShopProduct',)


class ShopProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop_group = models.ForeignKey(
        to=ShopGroup,
        on_delete=models.CASCADE,
    )
    categories = models.ManyToManyField(ShopProductCategory)
    created_at = models.DateTimeField(auto_now_add=True)
