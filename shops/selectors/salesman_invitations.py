from uuid import UUID

from core.exceptions import ObjectDoesNotExistError
from shops.models import SalesmanInvitation

__all__ = ('get_salesman_invitation_by_id',)


def get_salesman_invitation_by_id(
        invitation_id: UUID,
) -> SalesmanInvitation:
    try:
        return (
            SalesmanInvitation.objects
            .select_related('shop', 'shop__group')
            .get(id=invitation_id)
        )
    except SalesmanInvitation.DoesNotExist:
        raise ObjectDoesNotExistError({'invitation_id': invitation_id})
