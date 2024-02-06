import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from telegram.models import Bot

__all__ = ('BotFactory',)


class BotFactory(DjangoModelFactory):

    class Meta:
        model = Bot

    id = factory.Sequence(lambda n: n)
    token = FuzzyText()
    name = factory.Faker('name')
    username = FuzzyText(suffix='bot')
    start_text = factory.Faker('text')
    start_text_client_web_app = factory.Faker('text')
