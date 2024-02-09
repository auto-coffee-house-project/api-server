from datetime import timedelta
from uuid import UUID

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from shops.models import SalesmanInvitation

__all__ = ('get_salesman_invitation_by_id', 'get_expired_salesman_invitations')


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


def get_expired_salesman_invitations() -> QuerySet[SalesmanInvitation]:
    now = timezone.now()
    expires_at = now - timedelta(
        seconds=settings.SALESMAN_INVITATION_LIFETIME_SECONDS,
    )
    return SalesmanInvitation.objects.filter(created_at__lt=expires_at)
