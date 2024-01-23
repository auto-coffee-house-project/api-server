import pytest

from telegram.models import User


@pytest.mark.parametrize(
    'first_name, last_name, expected',
    [
        ('John', 'Doe', 'John Doe'),
        ('John', None, 'John'),
    ],
)
def test_user_full_name_and_str(
        first_name: str,
        last_name: str,
        expected: str,
) -> None:
    user = User(first_name=first_name, last_name=last_name)
    assert user.full_name == expected == str(user)
