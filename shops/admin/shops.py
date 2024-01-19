from django.contrib import admin

from shops.models import Shop

__all__ = ('ShopAdmin',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass
