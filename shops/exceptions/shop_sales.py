from rest_framework import status

from core.exceptions import ApplicationError

__all__ = ('ShopSaleDeleteTimeExpiredError',)


class ShopSaleDeleteTimeExpiredError(ApplicationError):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'Sale deletion time expired'
