from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopAdmin

__all__ = ('is_shop_admin', 'get_shop_admin')


def get_shop_admin(
        *,
        user_id: int,
        shop_group_id: int | type[int],
) -> ShopAdmin:
    try:
        return (
            ShopAdmin.objects
            .select_related('shop', 'shop__group')
            .get(
                user_id=user_id,
                shop__group_id=shop_group_id,
            )
        )
    except ShopAdmin.DoesNotExist:
        raise ObjectDoesNotExistError({
            'user_id': user_id,
            'shop_group_id': shop_group_id,
        })


def is_shop_admin(
        *,
        user_id: int,
        shop_group_id: int | type[int],
) -> bool:
    return (
        ShopAdmin.objects
        .filter(user_id=user_id, shop__group_id=shop_group_id)
        .exists()
    )
