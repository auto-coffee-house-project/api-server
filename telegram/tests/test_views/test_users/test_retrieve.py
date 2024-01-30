from collections.abc import Callable

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from telegram.tests.factories import UserFactory
from telegram.views import UserRetrieveApi


@pytest.fixture
def view() -> Callable[..., Response]:
    return UserRetrieveApi.as_view()


@pytest.mark.django_db
def test_user_retrieve(rf, view: Callable[..., Response]) -> None:
    user = UserFactory()
    url = reverse('telegram:user-retrieve', kwargs={'user_id': user.id})
    request = rf.get(url)

    response = view(request, user_id=user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == user.id
    assert response.data['username'] == user.username
    assert response.data['first_name'] == user.first_name
    assert response.data['last_name'] == user.last_name
    assert 'created_at' in response.data
    assert set(response.data) == {
        'id',
        'username',
        'first_name',
        'last_name',
        'created_at',
    }
