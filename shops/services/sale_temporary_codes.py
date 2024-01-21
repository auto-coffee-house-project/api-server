from shops.models import SaleTemporaryCode

__all__ = (
    'delete_sale_temporary_code',
    'create_sale_temporary_code',
)


def delete_sale_temporary_code(
        *,
        shop_client_id: int,
        shop_group_id: int,
) -> None:
    SaleTemporaryCode.objects.filter(
        client_id=shop_client_id,
        group_id=shop_group_id,
    ).delete()


def create_sale_temporary_code(
        shop_client_id: int,
        shop_group_id: int,
) -> SaleTemporaryCode:
    """
    Create sale temporary code for client for specific shop group.

    Regenerate code if it already exists.
    """
    delete_sale_temporary_code(
        shop_client_id=shop_client_id,
        shop_group_id=shop_group_id,
    )
    return SaleTemporaryCode.objects.create(
        client_id=shop_client_id,
        group_id=shop_group_id,
    )
