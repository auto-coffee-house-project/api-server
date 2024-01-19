from django.db import models

from telegram.models.users import User

__all__ = ('ShopClient',)


class ShopClient(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
