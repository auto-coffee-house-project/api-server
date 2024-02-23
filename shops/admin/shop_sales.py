from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from shops.models import ShopSale

__all__ = ('ShopSaleAdmin',)


@admin.register(ShopSale)
class ShopSaleAdmin(ImportExportModelAdmin):
    list_filter = ('shop', 'is_free', 'employee', 'client')
    list_select_related = ('shop', 'client')
    list_display = ('shop', 'client', 'employee', 'is_free', 'created_at')
    readonly_fields = ('is_free',)
