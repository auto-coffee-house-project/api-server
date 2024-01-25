from django.contrib import admin

from shops.models import ShopSalesman, ShopSale

__all__ = ('ShopSalesmanAdmin',)


class SaleInline(admin.TabularInline):
    model = ShopSale
    extra = 0
    can_delete = False
    readonly_fields = ('shop', 'salesman', 'is_free', 'created_at', 'comment')


@admin.register(ShopSalesman)
class ShopSalesmanAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', 'shop')
    search_fields = ('user__id', 'user__name', 'user__username')
    search_help_text = 'User ID, name or username'
    ordering = ('-created_at',)
    list_display = ('user', 'shop', 'created_at')
    list_select_related = ('user', 'shop')
    list_filter = ('shop',)
    inlines = (SaleInline,)
