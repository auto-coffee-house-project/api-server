from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopAdmin

__all__ = ('get_shop_admin_by_user_id',)


def get_shop_admin_by_user_id(user_id: int) -> ShopAdmin:
    try:
        return ShopAdmin.objects.get(user_id=user_id)
    except ShopAdmin.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})
