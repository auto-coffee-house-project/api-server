import factory
from factory.django import DjangoModelFactory

from telegram.models import User

__all__ = ('UserFactory',)


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
