from celery import shared_task

from shops.selectors import (
    get_expired_employee_invitations,
    get_expired_sale_codes,
)


@shared_task
def remove_expired_sale_codes() -> None:
    get_expired_sale_codes().delete()


@shared_task
def remove_expired_invitations() -> None:
    get_expired_employee_invitations().delete()
