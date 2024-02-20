from uuid import uuid4

from django.db import models

from telegram.models.bots import Bot

__all__ = ('ShopGroup',)


def get_gift_photo_path(instance: 'ShopGroup', filename: str) -> str:
    file_extension = filename.split('.')[-1].lower()
    filename = f'{uuid4().hex}.{file_extension}'
    return f'{instance.id}/{filename}'


class ShopGroup(models.Model):
    name = models.CharField(max_length=255)
    bot = models.OneToOneField(
        to=Bot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    gift_name = models.CharField(max_length=64, default='Бесплатная чашка кофе')
    gift_photo = models.ImageField(
        upload_to=get_gift_photo_path,
        null=True,
        blank=True,
    )
    each_nth_cup_free = models.PositiveSmallIntegerField()
    is_menu_shown = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'shop group'
        verbose_name_plural = 'shop groups'

    def __str__(self) -> str:
        return self.name
