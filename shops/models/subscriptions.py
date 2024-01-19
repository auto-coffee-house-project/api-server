from django.db import models

from shops.models.shops import Shop

__all__ = ('Subscription',)


class Subscription(models.Model):
    shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
    )
    starts_at = models.DateField()
    ends_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
