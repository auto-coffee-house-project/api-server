from django.db import models

from telegram.models.bots import Bot

__all__ = ('ShopGroup',)


class ShopGroup(models.Model):
    name = models.CharField(max_length=255)
    bot = models.OneToOneField(
        to=Bot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
