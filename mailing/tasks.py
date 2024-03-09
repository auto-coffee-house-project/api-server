from celery import shared_task

from mailing.services import send_messages, send_photos
from shops.selectors import get_shop_client_user_ids
from shops.selectors.shops import get_shop_by_id
from telegram.services.bots import (
    TelegramBotApiConnection,
    build_keyboard_markup,
    closing_telegram_bot_api_http_client,
)


@shared_task
def create_mailing(
        *,
        shop_id: int,
        text: str,
        parse_mode: str,
        buttons_json: str,
        base64_photo: str | None,
):
    shop = get_shop_by_id(shop_id)
    keyboard_markup = build_keyboard_markup(buttons_json)

    chat_ids = get_shop_client_user_ids(shop.id)

    with closing_telegram_bot_api_http_client(shop.bot.token) as http_client:
        telegram_bot_api_connection = TelegramBotApiConnection(http_client)

        if base64_photo is not None:
            send_photos(
                chat_ids=chat_ids,
                telegram_bot_api_connection=telegram_bot_api_connection,
                base64_photo=base64_photo,
                text=text,
                parse_mode=parse_mode,
                reply_markup=keyboard_markup,
            )
        else:
            send_messages(
                chat_ids=chat_ids,
                telegram_bot_api_connection=telegram_bot_api_connection,
                text=text,
                parse_mode=parse_mode,
                reply_markup=keyboard_markup,
            )
