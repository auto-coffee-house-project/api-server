import factory
from factory.django import DjangoModelFactory

from shops.models import ShopClient
from shops.tests.factories.shops import ShopFactory
from telegram.tests.factories import UserFactory

__all__ = ('ShopClientFactory',)


class ShopClientFactory(DjangoModelFactory):
    class Meta:
        model = ShopClient

    user = factory.SubFactory(UserFactory)
    shop = factory.SubFactory(ShopFactory)
