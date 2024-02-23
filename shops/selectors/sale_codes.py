from datetime import timedelta

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from shops.models import SaleCode

__all__ = (
    'get_sale_code',
    'get_expired_sale_codes',
)


def get_sale_code(code: str) -> SaleCode:
    try:
        return (
            SaleCode.objects
            .select_related('client', 'client__user', 'shop')
            .get(code=code)
        )
    except SaleCode.DoesNotExist:
        raise ObjectDoesNotExistError({'code': code})


def get_expired_sale_codes() -> QuerySet[SaleCode]:
    now = timezone.now()
    codes_expire_at = now - timedelta(
        seconds=settings.SALE_TEMPORARY_CODE_LIFETIME_SECONDS,
    )
    return SaleCode.objects.filter(created_at__lt=codes_expire_at)
