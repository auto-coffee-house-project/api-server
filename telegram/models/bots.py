from django.db import models

__all__ = ('Bot',)


class Bot(models.Model):
    id = models.BigIntegerField(primary_key=True)
    token = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    start_text = models.TextField(
        max_length=4096,
        default=(
            'Привет! ☺️ Мы рады что ты с нами и в благодарность'
            ' мы готовы дарить тебе кофе бесплатно!\n'
            'Мы будем стараться, делать наш сервис все лучше и лучше,'
            ' чтобы тебе хотелось возвращаться к нам.'
            ' А сейчас нажми кнопку меню чтобы отметить'
            ' свою первую покупку кофе! ☕️'
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
