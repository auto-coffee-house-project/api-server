from django.contrib import admin

from shops.models import ShopClient

__all__ = ('ShopClientAdmin',)


@admin.register(ShopClient)
class ShopClientAdmin(admin.ModelAdmin):
    pass
