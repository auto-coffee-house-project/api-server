from django.contrib import admin

from shops.models import Shop

__all__ = ('ShopAdmin',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    autocomplete_fields = ('group',)
    search_help_text = 'Name or group name'
    search_fields = ('name', 'group')
    list_display = ('name', 'group', 'created_at')
    list_select_related = ('group',)
