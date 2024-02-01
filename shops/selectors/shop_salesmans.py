from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopSalesman

__all__ = (
    'get_shop_salesman',
    'is_shop_salesman',
)


def get_shop_salesman(
        *,
        user_id: int | type[int],
        shop_group_id: int | type[int],
) -> ShopSalesman:
    try:
        return (
            ShopSalesman.objects
            .select_related('shop', 'shop__group')
            .get(user_id=user_id, shop__group_id=shop_group_id)
        )
    except ShopSalesman.DoesNotExist:
        raise ObjectDoesNotExistError({
            'user_id': user_id,
            'shop_group_id': shop_group_id,
        })


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
