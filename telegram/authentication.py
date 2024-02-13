from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from telegram.selectors import get_bot_by_id

__all__ = ('BotAuthentication',)


class BotAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request: Request):
        try:
            bot_id = request.META['HTTP_BOT_ID']
        except KeyError:
            return

        try:
            bot_id = int(bot_id)
        except ValueError:
            raise AuthenticationFailed('Bot ID must be integer')

        bot = get_bot_by_id(bot_id)

        request.META['bot'] = bot

        return None, None
