from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from shops.models import Shop

__all__ = ('ShopAdmin',)


@admin.register(Shop)
class ShopAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    search_help_text = 'Name'
    autocomplete_fields = ('bot',)
    list_display = (
        'name',
        'bot',
        'start_text',
        'each_nth_sale_free',
        'created_at',
    )
    ordering = ('-created_at',)
    list_select_related = ('bot',)
