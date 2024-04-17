from django.db.models import QuerySet

from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopEmployee

__all__ = ('get_shop_employee', 'get_shop_employees', 'get_shop_employee_by_id')


def get_shop_employee_by_id(employee_id: int) -> ShopEmployee:
    try:
        return ShopEmployee.objects.get(id=employee_id)
    except ShopEmployee.DoesNotExist:
        raise ObjectDoesNotExistError({'employee_id': employee_id})


def get_shop_employee(
        *,
        user_id: int,
        shop_id: int | type[int],
) -> ShopEmployee:
    try:
        return (
            ShopEmployee.objects
            .select_related('shop')
            .get(user_id=user_id, shop_id=shop_id)
        )
    except ShopEmployee.DoesNotExist:
        raise ObjectDoesNotExistError({
            'user_id': user_id,
            'shop_id': shop_id,
        })


def get_shop_employees(shop_id: int) -> QuerySet[ShopEmployee]:
    return ShopEmployee.objects.filter(shop_id=shop_id)
