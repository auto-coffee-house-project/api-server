from uuid import uuid4

from django.db import models

from shops.models.shop_groups import ShopGroup
from shops.models.shop_product_categories import ShopProductCategory

__all__ = ('ShopProduct',)


def get_shop_product_photo_path(instance: 'ShopProduct', filename: str) -> str:
    file_extension = filename.split('.')[-1]
    filename = f'{uuid4().hex}.{file_extension}'
    return f'{instance.shop_group_id}/{filename}'


class ShopProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop_group = models.ForeignKey(
        to=ShopGroup,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        upload_to=get_shop_product_photo_path,
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField(
        to=ShopProductCategory,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
