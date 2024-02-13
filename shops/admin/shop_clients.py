from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from shops.models import ShopClient, ShopSale

__all__ = ('ShopClientAdmin',)


class SaleInline(admin.TabularInline):
    model = ShopSale
    extra = 0
    can_delete = False
    readonly_fields = ('shop', 'salesman', 'is_free', 'created_at', 'comment')


@admin.register(ShopClient)
class ShopClientAdmin(ImportExportModelAdmin):
    autocomplete_fields = ('user', 'shop_group')
    search_fields = ('user__id', 'user__first_name', 'user__username')
    search_help_text = 'User ID, name or username'
    ordering = ('-created_at',)
    list_display = ('user', 'shop_group', 'has_gift', 'created_at')
    list_select_related = ('user', 'shop_group')
    list_filter = ('shop_group', 'has_gift')
    inlines = (SaleInline,)
