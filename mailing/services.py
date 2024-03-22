import base64
import io
import json
import logging
from collections.abc import Iterable

from shops.models import Shop
from shops.selectors import get_shop_client_user_ids
from shops.selectors.shops import get_shop_by_id
from telegram.models import KeyboardMarkup
from telegram.services.bots import (
    TelegramBotApiConnection,
    build_keyboard_markup, closing_telegram_bot_api_http_client,
)

logger = logging.getLogger(__name__)


def parse_base64_photo(base64_photo: str) -> bytes:
    return base64.b64decode(base64_photo)


class MailingService:

    def __init__(
            self,
            *,
            telegram_bot_api_connection: TelegramBotApiConnection,
            parse_mode: str,
    ):
        self.__telegram_bot_api_connection = telegram_bot_api_connection
        self.__parse_mode = parse_mode

    def send_photo_via_bytes_io(
            self,
            base64_photo: str,
            chat_id: int,
            text: str,
            reply_markup: KeyboardMarkup,
    ) -> str | None:
        photo_bytes = parse_base64_photo(base64_photo)
        with io.BytesIO(photo_bytes) as photo_io:
            response = self.__telegram_bot_api_connection.send_photo_io(
                photo=photo_io,
                chat_id=chat_id,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=self.__parse_mode,
            )
        response_data = response.json()
        if not response_data.get('ok'):
            return
        photo_file_id = response_data['result']['photo'][-1]['file_id']
        return photo_file_id

    def send_photo(
            self,
            chat_id: int,
            photo_file_id: str,
            caption: str,
            reply_markup: KeyboardMarkup,
    ):
        response = self.__telegram_bot_api_connection.send_photo_via_file_id_or_url(
            chat_id=chat_id,
            photo=photo_file_id,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=self.__parse_mode,
        )


def send_photos(
        *,
        chat_ids: Iterable[int],
        telegram_bot_api_connection: TelegramBotApiConnection,
        base64_photo: str,
        text: str,
        parse_mode: str,
        reply_markup: KeyboardMarkup,
):
    mailing_service = MailingService(
        telegram_bot_api_connection=telegram_bot_api_connection,
        parse_mode=parse_mode,
    )
    photo_file_id: str | None = None

    for chat_id in chat_ids:
        if photo_file_id is None:
            photo_file_id = mailing_service.send_photo_via_bytes_io(
                base64_photo=base64_photo,
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
            )
        else:
            mailing_service.send_photo(
                chat_id=chat_id,
                photo_file_id=photo_file_id,
                caption=text,
                reply_markup=reply_markup,
            )


def send_messages(
        chat_ids: Iterable[int],
        telegram_bot_api_connection: TelegramBotApiConnection,
        text: str,
        parse_mode: str,
        reply_markup: KeyboardMarkup,
):
    for chat_id in chat_ids:
        telegram_bot_api_connection.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )


def start_mailing(
        shop: Shop,
        buttons_json: str,
        segregation_options_json: str,
        text: str,
        base64_photo: str | None,
        parse_mode: str | None,
) -> None:
    keyboard_markup = build_keyboard_markup(buttons_json)

    segregation_options = json.loads(segregation_options_json)

    logger.debug(
        'Creating mail: segregation options',
        extra={'segregation_options': segregation_options},
    )

    chat_ids = get_shop_client_user_ids(shop.id, segregation_options)

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
