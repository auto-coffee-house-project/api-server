from django.contrib import admin

from shops.models import ShopSale

__all__ = ('ShopSaleAdmin',)


@admin.register(ShopSale)
class ShopSaleAdmin(admin.ModelAdmin):
    pass
