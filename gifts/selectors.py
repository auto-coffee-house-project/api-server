from shops.models import ShopClient

__all__ = ('has_main_gift',)


def has_main_gift(client: ShopClient) -> bool:
    return client.gift_set.filter(is_main=True).exists()
