from collections.abc import Callable

import pytest
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from telegram.views import UserRetrieveCreateUpdateApi


@pytest.fixture
def url() -> str:
    return reverse('telegram:user-create')


@pytest.fixture
def view() -> Callable[[Request], Response]:
    return UserRetrieveCreateUpdateApi.as_view()


@pytest.mark.django_db
def test_user_create(rf, url: str, view: Callable[[Request], Response]) -> None:
    request_data = {
        'id': 123456,
        'username': 'test_username',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
    }
    request = rf.post(url, data=request_data, content_type='application/json')

    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] == request_data['id']
    assert response.data['username'] == request_data['username']
    assert response.data['first_name'] == request_data['first_name']
    assert response.data['last_name'] == request_data['last_name']
    assert set(response.data) == {
        'id',
        'username',
        'first_name',
        'last_name',
        'created_at',
    }
