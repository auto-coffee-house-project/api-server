from django.contrib import admin

from shops.models import ShopSalesman

__all__ = ('ShopSalesmanAdmin',)


@admin.register(ShopSalesman)
class ShopSalesmanAdmin(admin.ModelAdmin):
    pass
