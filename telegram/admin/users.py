from django.contrib import admin

from telegram.models import User

__all__ = ('UserAdmin',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
