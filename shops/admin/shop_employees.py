from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from shops.models import ShopEmployee, ShopSale

__all__ = ('ShopEmployeeAdmin',)


class SaleInline(admin.TabularInline):
    model = ShopSale
    extra = 0
    can_delete = False
    readonly_fields = ('shop', 'employee', 'is_free', 'created_at', 'comment')


@admin.register(ShopEmployee)
class ShopEmployeeAdmin(ImportExportModelAdmin):
    autocomplete_fields = ('user', 'shop')
    search_fields = ('user__id', 'user__name', 'user__username')
    search_help_text = 'User ID, name or username'
    ordering = ('-created_at',)
    list_display = ('user', 'shop', 'created_at')
    list_select_related = ('user', 'shop')
    list_filter = ('shop', 'is_admin')
    inlines = (SaleInline,)
