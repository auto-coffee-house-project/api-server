from django.contrib import admin

from shops.models import ShopProduct

__all__ = ('ShopProductAdmin',)


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('name', 'price', 'shop_group', 'created_at')
    list_select_related = ('shop_group',)
    list_filter = ('categories',)
