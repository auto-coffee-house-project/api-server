from django.core import exceptions as django_exceptions
from django.http import Http404
from rest_framework import exceptions as drf_exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler as drf_exception_handler

from core.exceptions import ApplicationError, ObjectDoesNotExistError

__all__ = ('exception_handler',)


def exception_handler(exc, context) -> Response | None:
    """
    {
        'message': 'Error message',
        'extra': {}
    }
    """
    if isinstance(exc, django_exceptions.ValidationError):
        exc = drf_exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = drf_exceptions.NotFound()

    if isinstance(exc, django_exceptions.PermissionDenied):
        exc = drf_exceptions.PermissionDenied()

    response = drf_exception_handler(exc, context)

    is_application_error = isinstance(exc, ApplicationError)
    is_response_exists = response is not None

    if not is_response_exists:
        if is_application_error:
            data = {
                'message': exc.default_code,
                'extra': context.extra,
                'ok': False,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {'detail': response.data}

    if isinstance(exc, ObjectDoesNotExistError):
        response.data['message'] = exc.default_code
        response.data['extra'] = response.data.pop('detail', None)
    elif isinstance(exc, drf_exceptions.ValidationError):
        response.data['message'] = 'Validation error'
        response.data['extra'] = {'fields': response.data.pop('detail', None)}
    else:
        response.data['message'] = exc.default_code
        response.data['extra'] = response.data.pop('detail', None)

    response.data['ok'] = False
    return response
