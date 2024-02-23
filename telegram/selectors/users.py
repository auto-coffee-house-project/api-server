from core.exceptions import ObjectDoesNotExistError
from shops.selectors import get_shop_employee
from telegram.models import User, UserRole

__all__ = ('get_user_role', 'get_user_by_id')


def get_user_role(
        user_id: int | type[int],
        shop_id: int | type[int],
) -> UserRole:
    try:
        employee = get_shop_employee(
            user_id=user_id,
            shop_id=shop_id,
        )
    except ObjectDoesNotExistError:
        return UserRole.CLIENT
    return UserRole.ADMIN if employee.is_admin else UserRole.SALESMAN


def get_user_by_id(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})
