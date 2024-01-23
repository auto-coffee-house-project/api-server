from rest_framework import status

from core.exceptions import ApplicationError

__all__ = (
    'SalesmanAndSaleCodeShopGroupsNotEqualError',
    'SaleTemporaryCodeExpiredError',
)


class SalesmanAndSaleCodeShopGroupsNotEqualError(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'Salesman and sale code shop groups not equal'


class SaleTemporaryCodeExpiredError(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'Sale temporary code expired'
