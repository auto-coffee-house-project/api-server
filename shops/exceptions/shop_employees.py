from rest_framework import status

from core.exceptions import ApplicationError

__all__ = (
    'ShopEmployeeAlreadyExistsError',
    'UserAlreadyShopAdminError',
    'UserIsNotAdminError',
)


class ShopEmployeeAlreadyExistsError(ApplicationError):
    default_code = 'User is already an employee'
    status_code = status.HTTP_409_CONFLICT


class UserAlreadyShopAdminError(ApplicationError):
    default_code = 'User is already shop admin'
    status_code = status.HTTP_409_CONFLICT


class UserIsNotAdminError(ApplicationError):
    default_code = 'User is not admin'
    status_code = status.HTTP_403_FORBIDDEN
