from rest_framework import permissions

from telegram.models import Bot

__all__ = ('HasBot',)


class HasBot(permissions.BasePermission):

    def has_permission(self, request, view):
        return isinstance(request.META.get('bot'), Bot)
