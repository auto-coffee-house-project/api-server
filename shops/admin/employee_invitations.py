from django.contrib import admin

from shops.models import EmployeeInvitation

__all__ = ('EmployeeInvitationAdmin',)


@admin.register(EmployeeInvitation)
class EmployeeInvitationAdmin(admin.ModelAdmin):
    pass
