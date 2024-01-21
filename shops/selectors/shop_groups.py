from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopGroup

__all__ = ('get_shop_group_by_bot_id',)


def get_shop_group_by_bot_id(bot_id: int) -> ShopGroup:
    try:
        return ShopGroup.objects.get(bot_id=bot_id)
    except ShopGroup.DoesNotExist:
        raise ObjectDoesNotExistError(
            f'ShopGroup with {bot_id=} does not exist',
            bot_id=bot_id,
        )
