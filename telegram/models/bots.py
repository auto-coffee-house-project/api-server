from django.db import models

__all__ = ('Bot',)


class Bot(models.Model):
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    start_text = models.TextField(max_length=4096, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
