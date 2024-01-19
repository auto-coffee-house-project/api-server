from django.db import models

__all__ = ('User',)


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self) -> str:
        if self.last_name is not None:
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    def __str__(self):
        return self.full_name
