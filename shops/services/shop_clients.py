from shops.models import ShopClient

__all__ = ('get_or_create_shop_client',)


def get_or_create_shop_client(user_id: int) -> tuple[ShopClient, bool]:
    try:
        return ShopClient.objects.get(user_id=user_id), False
    except ShopClient.DoesNotExist:
        return ShopClient.objects.create(user_id=user_id), True
