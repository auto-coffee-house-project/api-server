from rest_framework import status

from core.exceptions import ApplicationError

__all__ = ('SaleCodeExpiredError',)


class SaleCodeExpiredError(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'Sale temporary code expired'
