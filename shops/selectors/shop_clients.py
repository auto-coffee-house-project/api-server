from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopClient

__all__ = ('get_shop_client_by_user_id',)


def get_shop_client_by_user_id(user_id: int, bot_id: int) -> ShopClient:
    try:
        return (
            ShopClient.objects
            .select_related('user')
            .get(user_id=user_id, shop_group__bot_id=bot_id)
        )
    except ShopClient.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})
