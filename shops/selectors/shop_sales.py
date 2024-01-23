from shops.models import ShopSale, Shop

__all__ = ('count_client_purchases_in_shop_group',)


def count_client_purchases_in_shop_group(
        *,
        client_id: int,
        shop_group_id: int,
) -> int:
    shops = Shop.objects.filter(group_id=shop_group_id)
    sales = ShopSale.objects.filter(
        client_id=client_id,
        shop__in=shops,
    )
    return sales.count()
