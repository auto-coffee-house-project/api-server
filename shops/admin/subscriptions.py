from django.contrib import admin

from shops.models import Subscription

__all__ = ('SubscriptionAdmin',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
