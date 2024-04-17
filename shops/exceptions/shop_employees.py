from rest_framework import status

from core.exceptions import ApplicationError

__all__ = (
    'ShopEmployeeAlreadyExistsError',
    'UserIsNotAdminError',
    'UserIsEmployeeError',
)


class ShopEmployeeAlreadyExistsError(ApplicationError):
    default_code = 'User is already an employee'
    status_code = status.HTTP_409_CONFLICT


class UserIsNotAdminError(ApplicationError):
    default_code = 'User is not admin'
    status_code = status.HTTP_403_FORBIDDEN


class UserIsEmployeeError(ApplicationError):
    default_code = 'User is employee'
    status_code = status.HTTP_403_FORBIDDEN
