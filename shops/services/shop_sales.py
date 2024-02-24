from django.db import transaction
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from shops.exceptions import (
    ClientAlreadyHasGiftError,
    SaleCodeExpiredError,
    ShopSaleDeleteTimeExpiredError, UserIsEmployeeError,
)
from shops.models import (SaleCode, Shop, ShopClient, ShopEmployee, ShopSale)
from shops.selectors import count_client_purchases_in_shop_group

__all__ = (
    'delete_shop_sale',
    'create_shop_sale_by_code',
    'will_be_given_gift',
    'create_shop_sale_by_user_id',
)


def delete_shop_sale(shop_sale: ShopSale) -> None:
    now = timezone.now()
    if now > shop_sale.can_be_deleted_until:
        raise ShopSaleDeleteTimeExpiredError({'sale_id': shop_sale.id})
    shop_sale.delete()


def will_be_given_gift(
        *,
        shop: Shop,
        client_id: int | type[int],
) -> bool:
    sales_count = count_client_purchases_in_shop_group(
        client_id=client_id,
        shop_id=shop.id,
    )
    total_purchases_count = sales_count['total_purchases_count']
    has_any_purchase = total_purchases_count != 0
    current_cups_count = (total_purchases_count + 1) % shop.each_nth_sale_free
    return current_cups_count == 0 and has_any_purchase


def create_shop_sale_by_code(
        *,
        employee: ShopEmployee,
        sale_code: SaleCode,
) -> ShopSale:
    if employee.user_id == sale_code.client.user_id:
        raise UserIsEmployeeError({
            'shop_id': employee.shop_id,
            'user_id': employee.user_id,
        })

    if employee.shop_id != sale_code.shop_id:
        raise ObjectDoesNotExistError({
            'shop_id': sale_code.shop_id,
            'code': sale_code.code,
        })

    if sale_code.client.has_gift:
        raise ClientAlreadyHasGiftError({
            'client_user_id': sale_code.client.user_id,
        })

    if sale_code.is_expired:
        raise SaleCodeExpiredError({
            'shop_id': sale_code.shop_id,
            'code': sale_code.code,
        })

    is_free = will_be_given_gift(
        shop=employee.shop,
        client_id=sale_code.client_id,
    )

    with transaction.atomic():
        if is_free:
            sale_code.client.has_gift = True
            sale_code.client.save()
        shop_sale = ShopSale.objects.create(
            shop=employee.shop,
            client_id=sale_code.client_id,
            employee=employee,
            is_free=is_free,
        )
        sale_code.delete()

    return shop_sale


def create_shop_sale_by_user_id(
        *,
        client: ShopClient,
        employee: ShopEmployee,
) -> ShopSale:
    if employee.user_id == client.user_id:
        raise UserIsEmployeeError({
            'shop_id': employee.shop_id,
            'user_id': employee.user_id,
        })

    if client.has_gift:
        raise ClientAlreadyHasGiftError({'client_user_id': client.user_id})

    is_free = will_be_given_gift(
        shop=client.shop,
        client_id=client.id,
    )
    if is_free:
        client.has_gift = True
        client.save()

    return ShopSale.objects.create(
        shop=client.shop,
        client=client,
        employee=employee,
        is_free=is_free,
    )
