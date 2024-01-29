from shops.models import ShopClient, ShopGroup, ShopClientStatistics

from shops.selectors import count_client_purchases_in_shop_group

__all__ = ('get_or_create_shop_client', 'get_shop_client_statistics')


def get_or_create_shop_client(user_id: int) -> tuple[ShopClient, bool]:
    try:
        return ShopClient.objects.get(user_id=user_id), False
    except ShopClient.DoesNotExist:
        return ShopClient.objects.create(user_id=user_id), True


def get_shop_client_statistics(
        shop_client: ShopClient,
        shop_group: ShopGroup,
) -> ShopClientStatistics:
    total_purchases_count = count_client_purchases_in_shop_group(
        client_id=shop_client.id,
        shop_group_id=shop_group.id,
    )
    current_cups_count = total_purchases_count % shop_group.each_nth_cup_free

    return ShopClientStatistics(
        user_id=shop_client.user.id,
        shop_group_bot_id=shop_group.bot.id,
        purchases_count=total_purchases_count,
        each_nth_cup_free=shop_group.each_nth_cup_free,
        current_cups_count=current_cups_count,
    )
