from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from telegram.forms import BotAdminForm
from telegram.models import Bot

__all__ = ('BotAdmin',)


@admin.register(Bot)
class BotAdmin(ImportExportModelAdmin):
    readonly_fields = ('id', 'name', 'username')
    form = BotAdminForm
