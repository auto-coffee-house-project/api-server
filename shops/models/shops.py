from uuid import uuid4

from django.db import models

from telegram.models.bots import Bot

__all__ = ('Shop',)


def get_gift_photo_path(instance: 'Shop', filename: str) -> str:
    return f'{instance.id}/{filename}'


class Shop(models.Model):
    name = models.CharField(max_length=255)
    bot = models.OneToOneField(to=Bot, on_delete=models.CASCADE)
    gift_name = models.CharField(max_length=64)
    gift_photo = models.ImageField(
        upload_to=get_gift_photo_path,
        null=True,
        blank=True,
    )
    start_text = models.TextField(max_length=4096)
    each_nth_sale_free = models.PositiveSmallIntegerField()
    is_menu_shown = models.BooleanField(default=False)
    subscription_starts_at = models.DateTimeField()
    subscription_ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __str__(self) -> str:
        return self.name
