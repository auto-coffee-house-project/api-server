from django.contrib import admin

from telegram.forms import BotAdminForm
from telegram.models import Bot

__all__ = ('BotAdmin',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', 'username')
    form = BotAdminForm
