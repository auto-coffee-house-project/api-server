from django.contrib import admin

from shops.models import ShopGroup

__all__ = ('ShopGroupAdmin',)


@admin.register(ShopGroup)
class ShopGroupAdmin(admin.ModelAdmin):
    pass
