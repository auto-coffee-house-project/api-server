from django.db import transaction

from core.exceptions import ObjectDoesNotExistError
from shops.exceptions.shop_clients import ClientHasNoGiftError
from shops.models import GiftCode, ShopClient
from telegram.services.bots import send_gift_code_activated_messages

__all__ = ('refresh_gift_code', 'activate_gift_code')


@transaction.atomic
def refresh_gift_code(client: ShopClient) -> GiftCode:
    if not client.has_gift:
        raise ClientHasNoGiftError({'client_id': client.id})
    GiftCode.objects.filter(client=client).delete()
    return GiftCode.objects.create(client=client, shop_id=client.shop_id)


@transaction.atomic
def activate_gift_code(
        *,
        code: str,
        shop_id: int,
        employee_user_id: int,
) -> None:
    try:
        gift_code = (
            GiftCode.objects
            .select_related('client')
            .get(code=code, shop_id=shop_id)
        )
    except GiftCode.DoesNotExist:
        raise ObjectDoesNotExistError({'code': code})

    client = gift_code.client
    if not client.has_gift:
        raise ClientHasNoGiftError({'client_id': client.id})

    client.has_gift = False
    client.save()
    gift_code.delete()

    send_gift_code_activated_messages(
        bot=client.shop.bot,
        client_user_id=client.user_id,
        employee_user_id=employee_user_id,
    )
