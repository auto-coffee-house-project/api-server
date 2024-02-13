import json

import pytest
from rest_framework.reverse import reverse

from telegram.tests.factories import BotFactory
from telegram.views import BotRetrieveUpdateApi


@pytest.mark.django_db
def test_bot_retrieve_api_bot_exists(rf) -> None:
    bot = BotFactory()
    url = reverse('telegram:bot-retrieve', kwargs={'bot_id': bot.id})
    request = rf.get(url)

    response = BotRetrieveUpdateApi.as_view()(request, bot.id)

    assert response.status_code == 200
    assert json.dumps(response.data) == json.dumps({
        'ok': True,
        'result': {
            'id': bot.id,
            'name': bot.name,
            'token': bot.token,
            'username': bot.username,
            'start_text': bot.start_text,
            'start_text_client_web_app': bot.start_text_client_web_app,
            'created_at': f'{bot.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
        },
    })


@pytest.mark.django_db
def test_bot_retrieve_api_bot_does_not_exist(rf) -> None:
    url = reverse('telegram:bot-retrieve', kwargs={'bot_id': 1})
    request = rf.get(url)

    response = BotRetrieveUpdateApi.as_view()(request, 1)

    assert response.status_code == 404
    assert json.dumps(response.data) == json.dumps({
        'message': 'Does not exist',
        'extra': {
            'bot_id': '1',
        },
        'ok': False,
    })
