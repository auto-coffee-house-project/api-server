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
    autocomplete_fields = ('user',)
    search_fields = ('user__id', 'user__name', 'user__username')
    search_help_text = 'User ID, name or username'
    ordering = ('-created_at',)
    list_display = ('user', 'created_at')
    list_select_related = ('user',)
    inlines = (SaleInline,)
