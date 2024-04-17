from django.db import models
from django.db.models import CheckConstraint

__all__ = ('Bot',)


class Bot(models.Model):
    id = models.BigIntegerField(primary_key=True)
    token = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    start_text = models.TextField(max_length=4096)
    sale_created_text = models.TextField(
        max_length=4096,
        default=(
            '✅ Код успешно применен!\n'
            '🔥 Для получения подарка осталось'
            ' совершить ещё {count} покупок'
        ),
    )
    gift_given_text = models.TextField(
        max_length=4096,
        default='🎉 Поздравляем! Вы получили подарок!',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = (
            CheckConstraint(
                name='bot_sale_created_text_contains_count',
                check=models.Q(sale_created_text__contains='{count}'),
                violation_error_message=(
                    'Sale created text must contain "{count}"'
                ),
            ),
        )
