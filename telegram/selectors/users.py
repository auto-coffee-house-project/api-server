from typing import Literal

from core.exceptions import ObjectDoesNotExistError
from shops.selectors import (
    get_shop_admin_by_user_id,
    get_shop_salesman_by_user_id,
)

__all__ = ('get_user_role',)


def get_user_role(user_id: int) -> Literal['client', 'salesman', 'admin']:
    try:
        get_shop_admin_by_user_id(user_id)
    except ObjectDoesNotExistError:
        try:
            get_shop_salesman_by_user_id(user_id)
        except ObjectDoesNotExistError:
            role: Literal['client'] = 'client'
        else:
            role: Literal['salesman'] = 'salesman'
    else:
        role: Literal['admin'] = 'admin'
    return role
