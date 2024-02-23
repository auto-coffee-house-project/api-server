from django.db import transaction

from shops.models import SaleCode

__all__ = ('delete_sale_code', 'refresh_sale_code')


def delete_sale_code(*, client_id: int, shop_id: int) -> None:
    SaleCode.objects.filter(client_id=client_id, shop_id=shop_id).delete()


@transaction.atomic
def refresh_sale_code(client_id: int, shop_id: int) -> SaleCode:
    """
    Create sale code for client for specific shop group.
    Regenerate code if it already exists.
    """
    delete_sale_code(client_id=client_id, shop_id=shop_id)
    return SaleCode.objects.create(client_id=client_id, shop_id=shop_id)
