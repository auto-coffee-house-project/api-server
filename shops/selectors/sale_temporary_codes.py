from core.exceptions import ObjectDoesNotExistError
from shops.models import SaleTemporaryCode

__all__ = ('get_sale_temporary_code',)


def get_sale_temporary_code(code: str) -> SaleTemporaryCode:
    try:
        return SaleTemporaryCode.objects.get(code=code)
    except SaleTemporaryCode.DoesNotExist:
        raise ObjectDoesNotExistError(
            f'Sale temporary code by {code=} does not exist',
            code=code,
        )
