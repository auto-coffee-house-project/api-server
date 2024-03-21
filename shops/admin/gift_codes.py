from django.contrib import admin

from shops.models import GiftCode

__all__ = ('GiftCode',)


@admin.register(GiftCode)
class GiftCodeAdmin(admin.ModelAdmin):
    list_filter = ('shop',)
    list_display = ('code', 'shop', 'client')
    list_select_related = ('shop', 'client')

    def has_change_permission(self, request, obj=None):
        return False
