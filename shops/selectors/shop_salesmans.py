from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopSalesman

__all__ = ('get_shop_salesman_by_user_id',)


def get_shop_salesman_by_user_id(user_id: int) -> ShopSalesman:
    try:
        return ShopSalesman.objects.select_related('shop').get(user_id=user_id)
    except ShopSalesman.DoesNotExist:
        raise ObjectDoesNotExistError(
            f'Shop salesman by {user_id=} does not exist',
            user_id=user_id,
        )
