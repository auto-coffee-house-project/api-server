from django.db import models

__all__ = ('ShopProductCategory',)


class ShopProductCategory(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
