from django.contrib import admin

from shops.models import SaleCode

__all__ = ('SaleCodeAdmin',)


@admin.register(SaleCode)
class SaleCodeAdmin(admin.ModelAdmin):
    pass
