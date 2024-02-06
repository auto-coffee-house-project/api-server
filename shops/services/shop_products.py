from collections.abc import Iterable
from decimal import Decimal

from django.db import transaction

from shops.models import ShopProduct, ShopProductCategory, ShopProductPhoto

__all__ = ('create_shop_product',)


@transaction.atomic
def create_shop_product(
        name: str,
        price: Decimal,
        shop_group_id: int | type[int],
        category_ids: Iterable[int],
        photos: Iterable[dict],
) -> ShopProduct:
    product = ShopProduct.objects.create(
        name=name,
        price=price,
        shop_group_id=shop_group_id,
    )
    categories = ShopProductCategory.objects.filter(id__in=category_ids)
    product.categories.add(categories)

    product_photos = [
        ShopProductPhoto(
            product=product,
            url=photo['url'],
            is_main=photo['is_main'],
        ) for photo in photos
    ]
    ShopProductPhoto.objects.bulk_create(product_photos)

    return product
