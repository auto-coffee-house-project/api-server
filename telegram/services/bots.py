import contextlib
from collections.abc import Generator
from typing import NewType

import httpx

from telegram.exceptions import TelegramBotApiError

__all__ = ('get_telegram_bot_id',)

TelegramApiHttpClient = NewType('HttpClient', httpx.Client)


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


def get_telegram_bot_id(token: str) -> int:
    with closing_telegram_bot_api_http_client(token) as http_client:
        telegram_bot_api_connection = TelegramBotApiConnection(http_client)
        me = telegram_bot_api_connection.get_me()

    if not me['ok']:
        error_description = me.get('description', 'Unknown error')
        raise TelegramBotApiError(error_description)

    return me['result']['id']
