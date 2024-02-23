from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopProduct

__all__ = ('get_shop_product',)


def get_shop_product(
        *,
        shop_id: int | type[int],
        product_id: int,
) -> ShopProduct:
    try:
        return (
            ShopProduct.objects
            .prefetch_related('categories')
            .get(shop_id=shop_id, id=product_id)
        )
    except ShopProduct.DoesNotExist:
        raise ObjectDoesNotExistError({'product_id': product_id})
