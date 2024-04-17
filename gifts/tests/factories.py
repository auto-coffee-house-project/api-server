import factory
from factory.django import DjangoModelFactory

from gifts.models import Gift
from shops.tests.factories.clients import ShopClientFactory
from shops.tests.factories.shops import ShopFactory

__all__ = ('GiftFactory',)


class GiftFactory(DjangoModelFactory):
    class Meta:
        model = Gift

    client = factory.SubFactory(ShopClientFactory)
    shop = factory.SubFactory(ShopFactory)

