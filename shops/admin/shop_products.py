from django.contrib import admin

from shops.models import ShopProduct

__all__ = ('ShopProductAdmin',)


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('name', 'price', 'shop', 'created_at')
    list_select_related = ('shop',)
    list_filter = ('categories',)
