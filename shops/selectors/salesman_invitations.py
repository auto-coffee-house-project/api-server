from datetime import timedelta
from uuid import UUID

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from shops.models import EmployeeInvitation

__all__ = ('get_employee_invitation', 'get_expired_employee_invitations')


def get_employee_invitation(invitation_id: UUID) -> EmployeeInvitation:
    try:
        return (
            EmployeeInvitation.objects
            .select_related('shop')
            .get(id=invitation_id)
        )
    except EmployeeInvitation.DoesNotExist:
        raise ObjectDoesNotExistError({'invitation_id': invitation_id})


def get_expired_employee_invitations() -> QuerySet[EmployeeInvitation]:
    now = timezone.now()
    expires_at = now - timedelta(
        seconds=settings.SALESMAN_INVITATION_LIFETIME_SECONDS,
    )
    return EmployeeInvitation.objects.filter(created_at__lt=expires_at)
