from shops.models import SalesmanInvitation, ShopAdmin

__all__ = ('create_salesman_invitation',)


def create_salesman_invitation(shop_admin: ShopAdmin) -> SalesmanInvitation:
    return SalesmanInvitation.objects.create(
        shop_id=shop_admin.shop_id,
        created_by_admin=shop_admin,
    )
