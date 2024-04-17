from django.contrib import admin

from shops.models import SaleCode

__all__ = ('SaleCodeAdmin',)


@admin.register(SaleCode)
class SaleCodeAdmin(admin.ModelAdmin):
    search_fields = ('code', 'shop', 'client')
    search_help_text = 'You can search by code, shop, and client.'
    list_display = ('code', 'shop', 'client', 'is_active', 'created_at')
    list_select_related = ('shop', 'client')
    list_filter = ('shop',)
    ordering = '-created_at',

    @admin.display(boolean=True)
    def is_active(self, obj: SaleCode) -> bool:
        return not obj.is_expired
