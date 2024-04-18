from celery import shared_task

from gifts.selectors import get_expired_gifts


@shared_task
def remove_expired_gifts() -> None:
    get_expired_gifts().delete()
