from rest_framework import status

from core.exceptions import ApplicationError

__all__ = ('InvitationExpiredError',)


class InvitationExpiredError(ApplicationError):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'Salesman invitation expired'
