from dataclasses import dataclass

from django.db import transaction
from django.utils import timezone

from shops.exceptions import (
    ClientAlreadyHasGiftError,
    SaleCodeExpiredError,
    ShopSaleDeleteTimeExpiredError,
    UserIsEmployeeError,
)
from shops.models import SaleCode, Shop, ShopClient, ShopEmployee, ShopSale
from shops.selectors import count_client_purchases_in_shop_group
from telegram.models import Bot
from telegram.services.bots import send_sale_created_messages

__all__ = (
    'delete_shop_sale',
    'create_shop_sale_by_code',
    'create_shop_sale_by_user_id',
)


def delete_shop_sale(shop_sale: ShopSale) -> None:
    now = timezone.now()
    if now > shop_sale.can_be_deleted_until:
        raise ShopSaleDeleteTimeExpiredError({'sale_id': shop_sale.id})
    shop_sale.delete()


def validate_user_is_not_employee(
        *,
        employee: ShopEmployee,
        client_user_id: int | type[int],
) -> None:
    if employee.user_id == client_user_id:
        raise UserIsEmployeeError({
            'shop_id': employee.shop_id,
            'user_id': employee.user_id,
        })


def validate_client_has_no_gift(client: ShopClient) -> None:
    if client.has_gift:
        raise ClientAlreadyHasGiftError({
            'user_id': client.user_id,
            'shop_id': client.shop_id,
        })


def validate_sale_code_is_not_expired(sale_code: SaleCode) -> None:
    if sale_code.is_expired:
        raise SaleCodeExpiredError({
            'shop_id': sale_code.shop_id,
            'code': sale_code.code,
        })


@dataclass(slots=True)
class PurchasesStatistics:
    each_nth_sale_free: int
    total_purchases_count: int

    def increment_total_purchases_count(self) -> None:
        self.total_purchases_count += 1

    @property
    def has_any_purchase(self) -> bool:
        return self.total_purchases_count > 0

    @property
    def purchases_progress(self) -> int:
        """
        Current progress of purchases for the next gift.

        **It will never be greater or equal to sales count required for the gift.**

        Returns:
            0 - if the gift is given. Otherwise - the progress.
        """
        return self.total_purchases_count % self.each_nth_sale_free

    @property
    def purchases_until_gift(self) -> int:
        return self.each_nth_sale_free - self.purchases_progress

    @property
    def will_be_gift_given(self) -> bool:
        """
        Check if on the next sale client will be given a gift.
        """
        progress_after_another_sale_created = self.purchases_progress + 1
        return progress_after_another_sale_created == self.each_nth_sale_free

    @property
    def is_gift_given(self) -> bool:
        return self.purchases_progress == 0


def create_shop_sale(
        *,
        bot: Bot,
        shop: Shop,
        client: ShopClient,
        employee: ShopEmployee,
) -> ShopSale:
    validate_user_is_not_employee(
        employee=employee,
        client_user_id=client.user_id,
    )
    validate_client_has_no_gift(client)

    sales_count = count_client_purchases_in_shop_group(
        client_id=client.id,
        shop_id=shop.id,
    )
    total_purchases_count = sales_count['total_purchases_count']

    purchases_statistics = PurchasesStatistics(
        each_nth_sale_free=shop.each_nth_sale_free,
        total_purchases_count=total_purchases_count,
    )

    shop_sale = ShopSale.objects.create(
        shop=shop,
        client_id=client.id,
        employee=employee,
        is_free=purchases_statistics.will_be_gift_given,
    )
    purchases_statistics.increment_total_purchases_count()

    if purchases_statistics.is_gift_given:
        client.has_gift = True
        client.save()

    send_sale_created_messages(
        bot=bot,
        client_user_id=client.user_id,
        employee_user_id=employee.user_id,
        is_gift_given=purchases_statistics.is_gift_given,
        sale_id=shop_sale.id,
        purchases_until_gift=purchases_statistics.purchases_until_gift,
    )

    return shop_sale


@transaction.atomic
def create_shop_sale_by_code(
        *,
        employee: ShopEmployee,
        sale_code: SaleCode,
) -> ShopSale:
    """

    It is assumed that sale code belongs to the same shop as employee.

    Keyword Args:
        employee: ShopEmployee instance.
        sale_code: SaleCode instance.

    Returns:
        ShopSale instance.
    """
    client = sale_code.client
    shop = sale_code.shop
    bot = shop.bot

    validate_sale_code_is_not_expired(sale_code)

    shop_sale = create_shop_sale(
        bot=bot,
        shop=shop,
        client=client,
        employee=employee,
    )
    sale_code.delete()

    return shop_sale


@transaction.atomic
def create_shop_sale_by_user_id(
        *,
        client: ShopClient,
        employee: ShopEmployee,
) -> ShopSale:
    shop = employee.shop
    bot = shop.bot

    return create_shop_sale(
        bot=bot,
        shop=shop,
        client=client,
        employee=employee,
    )
