from django.db import models

__all__ = ('Bot',)


class Bot(models.Model):
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
