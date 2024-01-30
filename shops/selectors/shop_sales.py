from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopSale, Shop

__all__ = (
    'count_client_purchases_in_shop_group',
    'get_shop_sale_by_id',
)


def count_client_purchases_in_shop_group(
        *,
        client_id: int | type[int],
        shop_group_id: int | type[int],
) -> int:
    shops = Shop.objects.filter(group_id=shop_group_id)
    sales = ShopSale.objects.filter(
        client_id=client_id,
        shop__in=shops,
    )
    return sales.count()


def get_shop_sale_by_id(sale_id: int) -> ShopSale:
    try:
        return ShopSale.objects.get(id=sale_id)
    except ShopSale.DoesNotExist:
        raise ObjectDoesNotExistError({'sale_id': sale_id})
