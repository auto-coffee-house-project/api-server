from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopClient

__all__ = (
    'get_shop_client',
    'get_shop_client_user_ids',
    'get_segregated_shop_client_user_ids',
)


def get_shop_client(user_id: int, shop_id: int) -> ShopClient:
    try:
        return (
            ShopClient.objects
            .select_related('user', 'shop')
            .get(user_id=user_id, shop_id=shop_id)
        )
    except ShopClient.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})


def get_shop_client_user_ids(shop_id: int) -> set[int]:
    shop_clients = ShopClient.objects.filter(shop_id=shop_id)
    user_ids = shop_clients.values_list('user_id', flat=True)
    return set(user_ids)


def get_segregated_shop_client_user_ids(
        shop_id: int,
        last_n_days_count: int,
        required_purchases_count: int,
) -> list[int]:
    from_date = timezone.now() - timedelta(days=last_n_days_count)
    shop_clients = ShopClient.objects.filter(shop_id=shop_id)
    return (
        shop_clients.filter(shopsale__created_at__gte=from_date)
        .annotate(purchases_count=Count('shopsale'))
        .filter(purchases_count__gte=required_purchases_count)
        .values_list('user_id', flat=True)
    )
