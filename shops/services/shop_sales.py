from django.db import transaction
from django.utils import timezone

from shops.exceptions import (
    ShopSaleDeleteTimeExpiredError,
    SalesmanAndSaleCodeShopGroupsNotEqualError,
    SaleTemporaryCodeExpiredError,
    UserIsNotShopClientError,
)
from shops.models import (
    ShopSale,
    ShopSalesman,
    SaleTemporaryCode,
    ShopGroup,
    ShopClient,
)
from shops.selectors import count_client_purchases_in_shop_group
from telegram.selectors import get_user_role

__all__ = (
    'delete_shop_sale',
    'create_shop_sale_by_code',
    'is_shop_sale_free',
    'create_shop_sale_by_user_id',
)


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
    has_any_purchase = sales_count != 0
    current_cups_count = (sales_count + 1) % shop_group.each_nth_cup_free
    return current_cups_count == 0 and has_any_purchase


def create_shop_sale_by_code(
        *,
        salesman: ShopSalesman,
        sale_temporary_code: SaleTemporaryCode,
) -> ShopSale:
    role = get_user_role(
        user_id=sale_temporary_code.client.user_id,
        shop_group_id=sale_temporary_code.group_id,
    )

    if role != 'client':
        raise UserIsNotShopClientError({
            'user_id': sale_temporary_code.client.user_id,
            'role': role,
        })

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


def create_shop_sale_by_user_id(
        *,
        shop_client: ShopClient,
        shop_salesman: ShopSalesman,
) -> ShopSale:
    is_free = is_shop_sale_free(
        shop_group=shop_salesman.shop.group,
        client_id=shop_client.id,
    )

    return ShopSale.objects.create(
        shop=shop_salesman.shop,
        client=shop_client,
        salesman=shop_salesman,
        is_free=is_free,
    )
