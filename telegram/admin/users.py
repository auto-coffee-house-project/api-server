from django.contrib import admin

from telegram.models import User

__all__ = ('UserAdmin',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'id',
        'username',
        'first_name',
        'last_name',
    )
    search_help_text = 'You can search by id, username, first name, last name'
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'created_at',
    )
    list_display_links = (
        'id',
        'username',
        'first_name',
        'last_name',
    )
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        return ('id',) if obj else ()
