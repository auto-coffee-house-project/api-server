from django.contrib import admin

from shops.models import ShopSale

__all__ = ('ShopSaleAdmin',)


@admin.register(ShopSale)
class ShopSaleAdmin(admin.ModelAdmin):
    list_filter = ('shop', 'is_free', 'salesman', 'client')
    list_select_related = ('shop', 'client')
    list_display = ('shop', 'client', 'salesman', 'is_free')
