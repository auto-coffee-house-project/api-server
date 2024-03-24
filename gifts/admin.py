from django.contrib import admin

from gifts.models import Gift

__all__ = ('GiftAdmin',)


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    pass
