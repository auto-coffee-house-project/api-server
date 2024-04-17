from typing import Any

from core.services import base64_to_in_memory_uploaded_file
from shops.models import Shop

__all__ = ('update_shop',)


def update_shop(
        shop: Shop,
        fields: dict[str, Any],
        gift_photo_in_base64: str,
) -> Shop:
    if 'gift_photo' in fields:
        gift_photo = base64_to_in_memory_uploaded_file(gift_photo_in_base64)
        shop.gift_photo = gift_photo

    if 'gift_name' in fields:
        shop.gift_name = fields['gift_name']

    if 'each_nth_sale_free' in fields:
        shop.each_nth_sale_free = fields['each_nth_sale_free']

    if 'birthdays_offer_after_nth_sale' in fields:
        shop.birthdays_offer_after_nth_sale = (
            fields['birthdays_offer_after_nth_sale']
        )

    if 'start_text' in fields:
        shop.start_text = fields['start_text']

    if 'is_menu_shown' in fields:
        shop.is_menu_shown = fields['is_menu_shown']

    shop.save()
    return shop
