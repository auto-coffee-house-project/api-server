from django.db import transaction

from shops.exceptions import (
    InvitationExpiredError,
    ShopSalesmanAlreadyExistsError,
)
from shops.models import ShopSalesman, SalesmanInvitation
from shops.selectors import is_salesman

__all__ = ('create_salesman_by_invitation',)


@transaction.atomic
def create_salesman_by_invitation(
        *,
        user_id: int,
        invitation: SalesmanInvitation,
) -> ShopSalesman:
    """
    Create salesman by special invitation link created by admin of shop.

    Keyword Args:
        user_id: ID of user who will be a salesman.
        invitation: SalesmanInvitation instance.

    Returns:
        ShopSalesman instance.

    Raises:
        InvitationExpiredError: If invitation is expired.
    """
    if invitation.is_expired:
        raise InvitationExpiredError({'invitation_id': invitation.id})

    if is_salesman(user_id):
        raise ShopSalesmanAlreadyExistsError({'user_id': user_id})

    invitation.delete()

    return ShopSalesman.objects.create(
        shop_id=invitation.shop_id,
        user_id=user_id,
    )
