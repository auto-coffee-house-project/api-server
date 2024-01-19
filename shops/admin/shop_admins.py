from django.contrib import admin

from shops.models import ShopAdmin

__all__ = ('ShopAdminAdmin',)


@admin.register(ShopAdmin)
class ShopAdminAdmin(admin.ModelAdmin):
    pass
