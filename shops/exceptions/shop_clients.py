from rest_framework import status

from core.exceptions import ApplicationError

__all__ = ('UserIsNotShopClientError',)


class UserIsNotShopClientError(ApplicationError):
    default_code = 'User is not shop client'
    status_code = status.HTTP_400_BAD_REQUEST
