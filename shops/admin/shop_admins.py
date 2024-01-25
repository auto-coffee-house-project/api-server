from django.contrib import admin

from shops.models import ShopAdmin

__all__ = ('ShopAdminAdmin',)


@admin.register(ShopAdmin)
class ShopAdminAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', 'shop')
    search_fields = ('user__id', 'user__name', 'user__username')
    search_help_text = 'User ID, name or username'
    ordering = ('-created_at',)
    list_display = ('user', 'shop', 'created_at')
    list_select_related = ('user', 'shop')
    list_filter = ('shop',)
