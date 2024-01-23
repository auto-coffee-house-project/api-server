from datetime import timedelta

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from shops.models import SaleTemporaryCode

__all__ = (
    'get_sale_temporary_code',
    'get_expired_sale_temporary_codes',
)


def get_sale_temporary_code(code: str) -> SaleTemporaryCode:
    try:
        return SaleTemporaryCode.objects.get(code=code)
    except SaleTemporaryCode.DoesNotExist:
        raise ObjectDoesNotExistError({'code': code})


def get_expired_sale_temporary_codes() -> QuerySet[SaleTemporaryCode]:
    now = timezone.now()
    codes_expire_at = now - timedelta(
        seconds=settings.SALE_TEMPORARY_CODE_LIFETIME_SECONDS,
    )
    return SaleTemporaryCode.objects.filter(created_at__lt=codes_expire_at)
