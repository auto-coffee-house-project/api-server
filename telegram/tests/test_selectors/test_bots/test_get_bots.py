import pytest

from telegram.selectors import get_bots
from telegram.tests.factories import BotFactory


@pytest.mark.django_db
def test_get_bots_count():
    BotFactory.create_batch(3)
    assert get_bots().count() == 3


@pytest.mark.django_db
def test_get_bots_order():
    BotFactory.create_batch(5)
    assert list(get_bots()) == list(get_bots().order_by('created_at'))


@pytest.mark.django_db
def test_no_bots():
    assert get_bots().count() == 0
