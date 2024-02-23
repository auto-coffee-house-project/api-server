from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from shops.models import Shop
from telegram.tests.factories.bots import BotFactory

__all__ = ('ShopFactory',)


class ShopFactory(DjangoModelFactory):
    class Meta:
        model = Shop

    name = Faker('name')
    bot = SubFactory(BotFactory)
    gift_name = Faker('name')
    gift_photo = None
    each_nth_cup_free = Faker('random_int', min=1, max=10)
    is_menu_shown = Faker('boolean')
    subscription_starts_at = Faker('date')
    subscription_ends_at = Faker('date')
