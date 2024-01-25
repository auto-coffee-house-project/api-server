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
    each_nth_cup_free = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'shop group'
        verbose_name_plural = 'shop groups'

    def __str__(self) -> str:
        return self.name
