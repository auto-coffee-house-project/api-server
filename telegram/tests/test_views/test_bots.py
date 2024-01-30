import json

import pytest
from rest_framework.response import Response
from rest_framework.reverse import reverse

from telegram.tests.factories import BotFactory
from telegram.views import BotListApi


@pytest.fixture
def url() -> str:
    return reverse('telegram:bot-list')


@pytest.mark.django_db
def test_bots_list_api_empty_response(rf, url: str) -> None:
    request = rf.get(url)

    response: Response = BotListApi.as_view()(request)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_bots_list_api(rf, url: str) -> None:
    bot = BotFactory()
    request = rf.get(url)

    response: Response = BotListApi.as_view()(request)

    assert response.status_code == 200
    assert json.dumps(response.data) == json.dumps([
        {
            'id': bot.id,
            'token': bot.token,
            'name': bot.name,
            'username': bot.username,
            'start_text': bot.start_text,
            'created_at': f'{bot.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
        }
    ])
