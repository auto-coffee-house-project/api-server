from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopClient

__all__ = ('get_shop_client', 'get_shop_client_user_ids')


def get_shop_client(user_id: int, shop_id: int) -> ShopClient:
    try:
        return (
            ShopClient.objects
            .select_related('user')
            .get(user_id=user_id, shop_id=shop_id)
        )
    except ShopClient.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})


def get_shop_client_user_ids(shop_id: int) -> set[int]:
    shop_clients = ShopClient.objects.filter(shop_id=shop_id)
    user_ids = shop_clients.values_list('user_id', flat=True)
    return set(user_ids)
