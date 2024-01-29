import contextlib
from collections.abc import Generator, Iterable
from typing import NewType, TypedDict

import httpx

from telegram.exceptions import TelegramBotApiError

__all__ = ('get_telegram_bot', 'send_messages')

TelegramApiHttpClient = NewType('HttpClient', httpx.Client)


class Bot(TypedDict):
    id: int
    first_name: str
    username: str


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

    def send_message(self, chat_id: int, text: str):
        url = '/sendMessage'
        request_data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
        }
        self.__http_client.post(url, json=request_data)


def get_telegram_bot(token: str) -> Bot:
    with closing_telegram_bot_api_http_client(token) as http_client:
        telegram_bot_api_connection = TelegramBotApiConnection(http_client)
        me = telegram_bot_api_connection.get_me()

    if not me['ok']:
        error_description = me.get('description', 'Unknown error')
        raise TelegramBotApiError(error_description)

    return me['result']


def send_messages(token: str, chat_ids: Iterable[int], text: str) -> None:
    with closing_telegram_bot_api_http_client(token) as http_client:
        telegram_bot_api_connection = TelegramBotApiConnection(http_client)

        for chat_id in chat_ids:
            telegram_bot_api_connection.send_message(chat_id, text)
