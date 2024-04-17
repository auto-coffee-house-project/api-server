from datetime import datetime
from typing import NotRequired, TypedDict

from django.db.models import Count
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopClient

__all__ = (
    'get_shop_client',
    'get_shop_client_user_ids',
)


class FromDateAndToDate(TypedDict):
    from_date: str
    to_date: str


class SegregationByBirthdays(FromDateAndToDate):
    pass


class SegregationByPurchases(FromDateAndToDate):
    purchases_count: int


class SegregationOptions(TypedDict):
    by_birthdays: NotRequired[SegregationByBirthdays]
    by_purchases: NotRequired[SegregationByPurchases]


def get_shop_client(user_id: int, shop_id: int) -> ShopClient:
    try:
        return (
            ShopClient.objects
            .select_related('user', 'shop')
            .get(user_id=user_id, shop_id=shop_id)
        )
    except ShopClient.DoesNotExist:
        raise ObjectDoesNotExistError({'user_id': user_id})


def get_shop_client_user_ids(
        shop_id: int,
        segregation_options: SegregationOptions,
) -> set[int]:
    segregation_by_birthdays = segregation_options.get('by_birthdays')
    segregation_by_purchases = segregation_options.get('by_purchases')

    shop_clients = ShopClient.objects.filter(shop_id=shop_id)

    if segregation_by_purchases is not None:
        now = timezone.now()
        purchases_count = segregation_by_purchases['purchases_count']
        from_date = datetime.fromisoformat(
            segregation_by_purchases['from_date'])
        to_date = datetime.fromisoformat(segregation_by_purchases['to_date'])

        from_date = now.replace(
            year=from_date.year,
            month=from_date.month,
            day=from_date.day,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        to_date = now.replace(
            year=to_date.year,
            month=to_date.month,
            day=to_date.day,
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )

        shop_clients = (
            shop_clients
            .annotate(purchases_count=Count('shopsale'))
            .filter(
                shopsale__created_at__gte=from_date,
                shopsale__created_at__lte=to_date,
                purchases_count__gte=purchases_count,
            )
        )

    if segregation_by_birthdays is not None:
        from_date = segregation_by_birthdays['from_date']
        to_date = segregation_by_birthdays['to_date']

        shop_clients = shop_clients.filter(
            born_on__gte=from_date,
            born_on__lte=to_date,
        )

    user_ids = shop_clients.values_list('user_id', flat=True)
    return set(user_ids)
