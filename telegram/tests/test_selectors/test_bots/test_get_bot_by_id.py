import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from core.exceptions import ObjectDoesNotExistError
from telegram.models import Bot
from telegram.selectors import get_bot_by_id
from telegram.tests.factories import BotFactory


@pytest.mark.django_db
def test_get_bot_by_id():
    bot: Bot = BotFactory()

    actual = get_bot_by_id(bot.id)

    assert actual.id == bot.id
    assert actual.name == bot.name
    assert actual.token == bot.token
    assert actual.created_at == bot.created_at
    assert actual.start_text == bot.start_text


@pytest.mark.django_db
def test_get_bot_by_id_not_found():
    with pytest.raises(ObjectDoesNotExistError) as error:
        get_bot_by_id(1)

    assert error.value.status_code == status.HTTP_404_NOT_FOUND
    assert error.value.detail == {
        'bot_id': ErrorDetail(string='1', code='Does not exist'),
    }
    assert error.value.default_code == 'Does not exist'
