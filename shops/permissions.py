from rest_framework import permissions
from rest_framework.request import Request

from telegram.models import Bot

__all__ = ('HasShop',)


class HasShop(permissions.BasePermission):

    def has_permission(self, request: Request, view) -> bool:
        bot: Bot | None = request.META.get('bot')
        return bot is not None and hasattr(bot, 'shop')
