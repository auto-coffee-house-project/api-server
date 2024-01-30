from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopSalesman

__all__ = ('get_shop_salesman_by_user_id', 'is_salesman')


def get_shop_salesman_by_user_id(user_id: int) -> ShopSalesman:
    try:
        return (
            ShopSalesman.objects
            .select_related('shop', 'shop__group')
            .get(user_id=user_id)
        )
    except ShopSalesman.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})


def is_salesman(user_id: int) -> bool:
    return ShopSalesman.objects.filter(user_id=user_id).exists()
