from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopSalesman

__all__ = ('get_shop_salesman_by_user_id', 'is_shop_salesman')


def get_shop_salesman_by_user_id(user_id: int) -> ShopSalesman:
    try:
        return (
            ShopSalesman.objects
            .select_related('shop', 'shop__group')
            .get(user_id=user_id)
        )
    except ShopSalesman.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})


def is_shop_salesman(
        *,
        user_id: int,
        shop_group_id: int | type[int],
) -> bool:
    return (
        ShopSalesman.objects
        .filter(user_id=user_id, shop__group_id=shop_group_id)
        .exists()
    )
