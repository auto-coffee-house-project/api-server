from django.db import models

from shops.models.shop_product_categories import ShopProductCategory
from shops.models.shops import Shop

__all__ = ('ShopProduct',)


def get_shop_product_photo_path(instance: 'ShopProduct', filename: str) -> str:
    return f'{instance.shop_id}/{filename}'


class ShopProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to=get_shop_product_photo_path,
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField(to=ShopProductCategory, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
