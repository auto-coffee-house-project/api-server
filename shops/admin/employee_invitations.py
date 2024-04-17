from django.contrib import admin

from shops.models import EmployeeInvitation

__all__ = ('EmployeeInvitationAdmin',)


@admin.register(EmployeeInvitation)
class EmployeeInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'is_active')
    list_select_related = ('shop',)
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'expires_at', 'is_active')

    @admin.display(boolean=True)
    def is_active(self, obj: EmployeeInvitation) -> bool:
        return not obj.is_expired
