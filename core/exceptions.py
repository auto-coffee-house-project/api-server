from rest_framework import status
from rest_framework.exceptions import APIException, NotFound


class ApplicationError(APIException):
    pass


class ObjectDoesNotExistError(NotFound):
    default_code = 'Does not exist'


class MessageBrokerConnectionError(ApplicationError):
    default_code = 'Message broker connection error'
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
