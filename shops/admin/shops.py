from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from shops.models import Shop, ShopAdmin

__all__ = ('ShopAdmin',)


class ShopAdminInline(admin.TabularInline):
    model = ShopAdmin
    extra = 0
    show_change_link = True


@admin.register(Shop)
class ShopAdmin(ImportExportModelAdmin):
    autocomplete_fields = ('group',)
    search_help_text = 'Name or group name'
    search_fields = ('name', 'group')
    list_display = ('name', 'group', 'created_at')
    list_select_related = ('group',)
    inlines = (ShopAdminInline,)
