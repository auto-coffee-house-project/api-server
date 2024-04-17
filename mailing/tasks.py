import logging

from celery import shared_task

from mailing.services import start_mailing
from shops.selectors.shops import get_shop_by_id

logger = logging.getLogger(__name__)


@shared_task
def start_mailing_task(
        *,
        shop_id: int,
        text: str,
        parse_mode: str | None,
        buttons_json: str,
        base64_photo: str | None,
        segregation_options_json: str,
):
    print(parse_mode)
    shop = get_shop_by_id(shop_id)

    start_mailing(
        shop=shop,
        text=text,
        parse_mode=parse_mode,
        buttons_json=buttons_json,
        base64_photo=base64_photo,
        segregation_options_json=segregation_options_json,
    )
