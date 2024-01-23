from rest_framework.reverse import reverse


def test_bot_list() -> None:
    assert reverse('telegram:bot-list') == '/api/telegram/bots/'


def test_user_create() -> None:
    assert reverse('telegram:user-create') == '/api/telegram/users/'


def test_user_retrieve() -> None:
    user_id = 1
    actual = reverse(
        'telegram:user-retrieve',
        kwargs={'user_id': user_id},
    )
    expected = f'/api/telegram/users/{user_id}/'
    assert actual == expected
