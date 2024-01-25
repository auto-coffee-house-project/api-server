from django.contrib import admin

from shops.models import ShopGroup, Shop

__all__ = ('ShopGroupAdmin',)


class ShopInline(admin.TabularInline):
    model = Shop
    extra = 0


@admin.register(ShopGroup)
class ShopGroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    search_help_text = 'Name'
    list_display = ('name', 'bot', 'each_nth_cup_free', 'created_at')
    ordering = ('-created_at',)
    list_select_related = ('bot',)
    inlines = (ShopInline,)
