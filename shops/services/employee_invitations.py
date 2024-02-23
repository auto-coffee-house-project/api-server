from uuid import UUID

from shops.exceptions import UserIsNotAdminError
from shops.models import EmployeeInvitation, ShopEmployee

__all__ = ('create_employee_invitation', 'build_invitation_url')


def create_employee_invitation(employee: ShopEmployee) -> EmployeeInvitation:
    if not employee.is_admin:
        raise UserIsNotAdminError({'user_id': employee.user_id})
    return EmployeeInvitation.objects.create(
        shop_id=employee.shop_id,
        created_by=employee,
    )


def build_invitation_url(
        *,
        bot_username: str,
        invitation_id: UUID,
) -> str:
    return f'https://t.me/{bot_username}'f'?start=invite-{invitation_id.hex}'
