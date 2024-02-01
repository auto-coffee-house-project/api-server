from rest_framework import status

from core.exceptions import ApplicationError

__all__ = ('ShopSalesmanAlreadyExistsError', 'UserAlreadyShopAdminError')


class ShopSalesmanAlreadyExistsError(ApplicationError):
    default_code = 'User is already salesman'
    status_code = status.HTTP_409_CONFLICT


class UserAlreadyShopAdminError(ApplicationError):
    default_code = 'User is already shop admin'
    status_code = status.HTTP_409_CONFLICT
