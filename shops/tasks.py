from celery import shared_task

from shops.selectors import (
    get_expired_employee_invitations,
    get_expired_sale_codes,
    get_shop_client_user_ids,
)
from shops.selectors.shops import get_shop_by_id
from telegram.services.bots import build_keyboard_markup, send_messages


@shared_task
def remove_expired_sale_codes() -> None:
    get_expired_sale_codes().delete()


@shared_task
def remove_expired_invitations() -> None:
    get_expired_employee_invitations().delete()


@shared_task
def start_mailing(
        shop_id: int,
        text: str,
        buttons_json: str,
) -> None:
    keyboard_markup = build_keyboard_markup(buttons_json)

    shop = get_shop_by_id(shop_id)
    user_ids = get_shop_client_user_ids(shop_id)

    send_messages(
        token=shop.bot.token,
        chat_ids=user_ids,
        text=text,
        reply_markup=keyboard_markup,
    )
