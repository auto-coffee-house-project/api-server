from django.contrib import admin

from shops.models import ShopProductCategory

__all__ = ('ShopProductCategoryAdmin',)


@admin.register(ShopProductCategory)
class ShopProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('created_at',)
