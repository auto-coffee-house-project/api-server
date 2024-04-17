from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from shops.models import ShopProduct
from shops.tests.factories.shops import ShopFactory

__all__ = ('ProductFactory',)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = ShopProduct

    name = Faker('name')
    price = Faker('random_number', digits=2)
    shop = SubFactory(ShopFactory)
    photo = None
