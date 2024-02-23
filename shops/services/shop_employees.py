from django.db import transaction

from core.exceptions import ObjectDoesNotExistError
from shops.exceptions import (
    InvitationExpiredError,
    ShopEmployeeAlreadyExistsError,
)
from shops.models import EmployeeInvitation, Shop, ShopEmployee
from shops.selectors import is_shop_employee

__all__ = ('create_employee_via_invitation', 'delete_shop_employee')


@transaction.atomic
def create_employee_via_invitation(
        *,
        user_id: int,
        invitation: EmployeeInvitation,
) -> ShopEmployee:
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

    if is_shop_employee(user_id=user_id, shop_id=invitation.shop_id):
        raise ShopEmployeeAlreadyExistsError({'user_id': user_id})

    invitation.delete()

    return ShopEmployee.objects.create(
        shop_id=invitation.shop_id,
        user_id=user_id,
    )


def delete_shop_employee(*, employee: ShopEmployee, shop: Shop):
    """
    Delete employee from shop.

    Args:
        employee: ShopEmployee instance.
        shop: Shop instance.

    Returns:
        True if employee was deleted successfully.
    """
    is_employee_belongs_to_shop = employee.shop_id == shop.id
    if not is_employee_belongs_to_shop:
        raise ObjectDoesNotExistError({'employee_id': employee.id})
    return employee.delete()
