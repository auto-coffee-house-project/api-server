import contextlib
import io
import json
from collections.abc import Generator
from typing import NewType, TypedDict

import httpx

from telegram.exceptions import TelegramBotApiError
from telegram.models import Bot, Button, KeyboardMarkup

__all__ = (
    'get_telegram_bot',
    'build_keyboard_markup',
    'send_sale_created_messages',
    'send_gift_code_activated_messages',
    'update_bot',
    'TelegramBotApiConnection',
)

TelegramApiHttpClient = NewType('HttpClient', httpx.Client)


class BotDict(TypedDict):
    id: int
    first_name: str
    username: str


def build_keyboard_markup(buttons_json: str) -> KeyboardMarkup:
    buttons: list[Button] = json.loads(buttons_json)
    return {'inline_keyboard': [[button] for button in buttons]}


@contextlib.contextmanager
def closing_telegram_bot_api_http_client(
        token: str,
) -> Generator[TelegramApiHttpClient, None, None]:
    base_url = f'https://api.telegram.org/bot{token}'
    with httpx.Client(base_url=base_url) as client:
        yield TelegramApiHttpClient(client)


class TelegramBotApiConnection:

    def __init__(self, http_client: TelegramApiHttpClient):
        self.__http_client = http_client

    def get_me(self) -> dict:
        url = '/getMe'
        response = self.__http_client.get(url)
        return response.json()

    def send_message(
            self,
            chat_id: int | type[int],
            text: str,
            parse_mode: str | None = None,
            reply_markup: KeyboardMarkup | None = None,
    ):
        url = '/sendMessage'
        request_data = {
            'chat_id': chat_id,
            'text': text,
        }
        if parse_mode:
            request_data['parse_mode'] = parse_mode
        if reply_markup:
            request_data['reply_markup'] = reply_markup
        self.__http_client.post(url, json=request_data)

    def send_photo_via_file_id_or_url(
            self,
            photo: str,
            chat_id: int,
            caption: str | None,
            parse_mode: str,
            reply_markup: KeyboardMarkup,
    ):
        url = '/sendPhoto'
        request_data = {
            'chat_id': chat_id,
            'photo': photo,
        }
        if caption:
            request_data['caption'] = caption
        if parse_mode:
            request_data['parse_mode'] = parse_mode
        if reply_markup:
            request_data['reply_markup'] = reply_markup
        return self.__http_client.post(url, json=request_data)

    def send_photo_io(
            self,
            photo: io.BytesIO,
            chat_id: int,
            caption: str | None,
            parse_mode: str,
            reply_markup: KeyboardMarkup,
    ):
        url = '/sendPhoto'
        request_files = {'photo': photo}
        request_data = {'chat_id': chat_id, }
        if caption:
            request_data['caption'] = caption
        if parse_mode:
            request_data['parse_mode'] = parse_mode
        if reply_markup:
            request_data['reply_markup'] = json.dumps(reply_markup)
        return self.__http_client.post(url, data=request_data,
                                       files=request_files)


def get_telegram_bot(token: str) -> BotDict:
    with closing_telegram_bot_api_http_client(token) as http_client:
        telegram_bot_api_connection = TelegramBotApiConnection(http_client)
        me = telegram_bot_api_connection.get_me()

    if not me['ok']:
        error_description = me.get('description', 'Unknown error')
        raise TelegramBotApiError(error_description)

    return me['result']


def build_sale_created_keyboard_markup(sale_id: int) -> KeyboardMarkup:
    return {
        'inline_keyboard': [
            [
                {
                    'text': '🔙 Отменить продажу',
                    'callback_data': f'sale-delete:{sale_id}'
                }
            ],
        ],
    }


def send_gift_code_activated_messages(
        *,
        bot: Bot,
        client_user_id: int | type[int],
        employee_user_id: int | type[int],
) -> None:
    with closing_telegram_bot_api_http_client(bot.token) as http_client:
        telegram_bot_api = TelegramBotApiConnection(http_client)

        telegram_bot_api.send_message(
            chat_id=employee_user_id,
            text=(
                '✅ Код успешно активирован.'
                ' Клиент может получить свой подарок!'
            ),
        )
        telegram_bot_api.send_message(
            chat_id=client_user_id,
            text=(
                f'✅ Код успешно активирован.'
                f' Можете забрать свой подарок!'
            ),
        )


def send_sale_created_messages(
        *,
        bot: Bot,
        client_user_id: int | type[int],
        employee_user_id: int | type[int],
        is_gift_given: bool,
        sale_id: int,
        purchases_until_gift: int,
) -> None:
    if is_gift_given:
        text_to_client = bot.gift_given_text
        text_to_employee = (
            '✅ Код успешно применен!\n'
            '🎉 Клиент получил подарок!'
        )
        reply_markup_to_employee = build_sale_created_keyboard_markup(sale_id)
    else:
        text_to_client = bot.sale_created_text.format(
            count=purchases_until_gift,
        )
        text_to_employee = '✅ Код успешно применен!'
        reply_markup_to_employee = build_sale_created_keyboard_markup(sale_id)

    with closing_telegram_bot_api_http_client(bot.token) as http_client:
        telegram_bot_api = TelegramBotApiConnection(http_client)

        telegram_bot_api.send_message(
            chat_id=employee_user_id,
            text=text_to_employee,
            reply_markup=reply_markup_to_employee,
        )
        telegram_bot_api.send_message(
            chat_id=client_user_id,
            text=text_to_client,
        )


def update_bot(
        bot: Bot,
        *,
        start_text: str,
        sale_created_text: str,
        gift_given_text: str,
) -> None:
    bot.start_text = start_text
    bot.sale_created_text = sale_created_text
    bot.gift_given_text = gift_given_text

    bot.full_clean()
    bot.save()
