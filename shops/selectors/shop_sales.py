from django.db.models import Case, Count, IntegerField, When

from core.exceptions import ObjectDoesNotExistError
from shops.models import ShopSale

__all__ = (
    'count_client_purchases_in_shop_group',
    'get_shop_sale_by_id',
)


def count_client_purchases_in_shop_group(
        *,
        client_id: int | type[int],
        shop_id: int | type[int],
) -> dict:
    return (
        ShopSale.objects
        .filter(client_id=client_id, shop_id=shop_id)
        .aggregate(
            total_purchases_count=Count('id'),
            free_purchases_count=Count(
                Case(
                    When(
                        is_free=True,
                        then=1,
                    ),
                    output_field=IntegerField(),
                )
            )
        )
    )


def get_shop_sale_by_id(sale_id: int) -> ShopSale:
    try:
        return ShopSale.objects.get(id=sale_id)
    except ShopSale.DoesNotExist:
        raise ObjectDoesNotExistError({'sale_id': sale_id})
