from rest_framework.exceptions import APIException, NotFound


class ApplicationError(APIException):
    pass


class ObjectDoesNotExistError(NotFound):
    default_code = 'Does not exist'
