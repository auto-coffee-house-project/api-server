from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from telegram.exceptions import TelegramBotApiError
from telegram.models import Bot
from telegram.services.bots import get_telegram_bot

__all__ = ('BotAdminForm',)


class BotAdminForm(forms.ModelForm):
    """Automatically get bot id from Telegram Bot API."""

    def clean(self):
        self.instance: Bot
        super().clean()

        token = self.cleaned_data['token']

        try:
            bot = get_telegram_bot(token)
        except TelegramBotApiError as error:
            raise ValidationError(
                _('Bot token error: %(error_description)s'),
                code='invalid',
                params={'error_description': error.description},
            )

        self.instance.id = bot['id']
        self.instance.name = bot['first_name']
        self.instance.username = bot['username']
