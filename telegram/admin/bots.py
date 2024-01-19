from django.contrib import admin

from telegram.models import Bot

__all__ = ('BotAdmin',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    pass
