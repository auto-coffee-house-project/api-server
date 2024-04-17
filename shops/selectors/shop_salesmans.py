from shops.models import ShopEmployee

__all__ = ('is_shop_employee',)


def is_shop_employee(
        *,
        user_id: int,
        shop_id: int | type[int],
) -> bool:
    return (
        ShopEmployee.objects
        .filter(user_id=user_id, shop_id=shop_id)
        .exists()
    )
