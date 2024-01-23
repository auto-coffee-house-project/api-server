from celery import shared_task

from shops.selectors import get_expired_sale_temporary_codes


@shared_task
def remove_expired_tasks() -> None:
    get_expired_sale_temporary_codes().delete()
