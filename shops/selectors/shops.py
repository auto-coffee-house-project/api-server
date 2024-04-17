from core.exceptions import ObjectDoesNotExistError
from shops.models import Shop

__all__ = ('get_shop_by_id',)


def get_shop_by_id(shop_id: int) -> Shop:
    try:
        return Shop.objects.select_related('bot').get(id=shop_id)
    except Shop.DoesNotExist:
        raise ObjectDoesNotExistError({'shop_id': shop_id})
