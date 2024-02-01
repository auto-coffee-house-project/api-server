from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopAdmin

__all__ = ('get_shop_admin_by_user_id', 'is_shop_admin')


def get_shop_admin_by_user_id(user_id: int) -> ShopAdmin:
    try:
        return ShopAdmin.objects.get(user_id=user_id)
    except ShopAdmin.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})


def is_shop_admin(
        *,
        user_id: int,
        shop_group_id: int,
) -> bool:
    return (
        ShopAdmin.objects
        .filter(user_id=user_id, shop__group_id=shop_group_id)
        .exists()
    )
