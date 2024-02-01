from typing import Literal

from core.exceptions import ObjectDoesNotExistError
from shops.selectors import is_shop_admin, is_shop_salesman
from telegram.models import User

__all__ = ('get_user_role', 'get_user_by_id')


def get_user_role(
        user_id: int | type[int],
        shop_group_id: int | type[int],
) -> Literal['client', 'salesman', 'admin']:
    if is_shop_admin(user_id=user_id, shop_group_id=shop_group_id):
        return 'admin'

    if is_shop_salesman(user_id=user_id, shop_group_id=shop_group_id):
        return 'salesman'

    return 'client'


def get_user_by_id(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})
