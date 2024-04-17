from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from telegram.forms import BotAdminForm
from telegram.models import Bot

__all__ = ('BotAdmin',)


@admin.register(Bot)
class BotAdmin(ImportExportModelAdmin):
    readonly_fields = ('id', 'name', 'username')
    search_fields = ('id', 'name', 'username')
    search_help_text = 'You can search by ID, name, username'
    form = BotAdminForm
