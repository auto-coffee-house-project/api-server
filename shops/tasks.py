from celery import shared_task

from shops.models import ShopSale
from shops.selectors import (
    get_expired_sale_temporary_codes,
    get_shop_admin, get_expired_salesman_invitations,
)
from telegram.services.bots import send_messages


@shared_task
def remove_expired_tasks() -> None:
    get_expired_sale_temporary_codes().delete()


@shared_task
def remove_expired_invitations() -> None:
    get_expired_salesman_invitations().delete()


@shared_task
def start_mailing(admin_user_id: int, shop_group_id: int, text: str) -> None:
    shop_admin = get_shop_admin(
        user_id=admin_user_id,
        shop_group_id=shop_group_id,
    )

    shop_user_ids = (
        ShopSale
        .objects
        .filter(shop=shop_admin.shop)
        .distinct('client__user_id')
        .values_list('client__user_id', flat=True)
    )

    send_messages(shop_admin.shop.group.bot.token, shop_user_ids, text)
