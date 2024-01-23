from django.db import transaction
from django.utils import timezone

from shops.exceptions import (
    ShopSaleDeleteTimeExpiredError,
    SalesmanAndSaleCodeShopGroupsNotEqualError,
    SaleTemporaryCodeExpiredError,
)
from shops.models import ShopSale, ShopSalesman, SaleTemporaryCode, ShopGroup
from shops.selectors import count_client_purchases_in_shop_group

__all__ = ('delete_shop_sale', 'create_shop_sale', 'is_shop_sale_free')


def delete_shop_sale(shop_sale: ShopSale) -> None:
    now = timezone.now()
    if now > shop_sale.can_be_deleted_until:
        raise ShopSaleDeleteTimeExpiredError({'sale_id': shop_sale.id})
    shop_sale.delete()


def is_shop_sale_free(
        *,
        shop_group: ShopGroup,
        client_id: int | type[int],
) -> bool:
    sales_count = count_client_purchases_in_shop_group(
        client_id=client_id,
        shop_group_id=shop_group.id,
    )
    return sales_count % shop_group.each_nth_cup_free == 0


def create_shop_sale(
        *,
        salesman: ShopSalesman,
        sale_temporary_code: SaleTemporaryCode,
) -> ShopSale:
    if salesman.shop.group_id != sale_temporary_code.group_id:
        raise SalesmanAndSaleCodeShopGroupsNotEqualError({
            'salesman_user_id': salesman.user_id,
            'code': sale_temporary_code.code,
        })

    if sale_temporary_code.is_expired:
        raise SaleTemporaryCodeExpiredError({'code': sale_temporary_code.code})

    is_free = is_shop_sale_free(
        shop_group=salesman.shop.group,
        client_id=sale_temporary_code.client_id,
    )

    with transaction.atomic():
        shop_sale = ShopSale.objects.create(
            shop=salesman.shop,
            client_id=sale_temporary_code.client_id,
            salesman=salesman,
            is_free=is_free,
        )
        sale_temporary_code.delete()

    return shop_sale
