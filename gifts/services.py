from datetime import datetime, timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from core.exceptions import ObjectDoesNotExistError
from gifts.exceptions import ClientAlreadyHasMainGiftError, GiftExpiredError
from gifts.models import Gift
from shops.models import Shop, ShopClient
from telegram.services.bots import send_gift_code_activated_messages

__all__ = ('GiftCreateContext', 'activate_gift')


class GiftCreateContext:

    def __init__(self, *, client: ShopClient, shop: Shop):
        self.__client = client
        self.__shop = shop

    @property
    def expires_at(self) -> datetime:
        now = timezone.now()
        return now + timedelta(seconds=settings.GIFT_CODE_LIFETIME_DAYS)

    def create_main_gift(self) -> Gift:
        is_main_gift_exists = (
            Gift.objects.filter(
                client=self.__client,
                is_main=True,
            )
        )
        if is_main_gift_exists:
            raise ClientAlreadyHasMainGiftError

        return Gift.objects.create(
            client=self.__client,
            shop=self.__shop,
            is_main=True,
            expires_at=self.expires_at,
        )

    def create_extra_gift(self) -> Gift:
        return Gift.objects.create(
            client=self.__client,
            shop=self.__shop,
            is_main=False,
            expires_at=self.expires_at,
        )


@transaction.atomic
def activate_gift(*, shop: Shop, code: str, employee_user_id: int) -> None:
    try:
        gift = (
            Gift.objects
            .select_related('client')
            .get(code=code, shop=shop)
        )
    except Gift.DoesNotExist:
        raise ObjectDoesNotExistError({'code': code})

    if gift.is_expired:
        raise GiftExpiredError({'code': code})

    gift.delete()

    send_gift_code_activated_messages(
        bot=shop.bot,
        client_user_id=gift.client.user_id,
        employee_user_id=employee_user_id,
    )
