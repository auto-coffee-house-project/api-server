from typing import TypeAlias, TypedDict

from django.db.models import Case, Count, IntegerField, When

from shops.models import (
    ClientUser,
    Shop,
    ShopClient,
    ShopClientStatistics,
    ShopSale,
)
from shops.selectors import count_client_purchases_in_shop_group

__all__ = (
    'get_or_create_shop_client',
    'get_shop_client_statistics',
    'get_shop_client_statistics_list',
)

IsCreated: TypeAlias = bool


class ClientPurchasesStatistics(TypedDict):
    client_id: int
    total_purchases_count: int
    free_purchases_count: int


def get_or_create_shop_client(
        *,
        user_id: int,
        shop_id: int,
) -> tuple[ShopClient, IsCreated]:
    return ShopClient.objects.get_or_create(
        user_id=user_id,
        shop_id=shop_id,
    )


def get_shop_client_statistics(
        shop_client: ShopClient,
        shop: Shop,
) -> ShopClientStatistics:
    client_purchases = count_client_purchases_in_shop_group(
        client_id=shop_client.id,
        shop_id=shop.id,
    )
    total_purchases_count = client_purchases['total_purchases_count']
    free_purchases_count = client_purchases['free_purchases_count']

    current_cups_count = total_purchases_count % shop.each_nth_sale_free

    return ShopClientStatistics(
        client_id=shop_client.id,
        user=ClientUser(
            id=shop_client.user.id,
            first_name=shop_client.user.first_name,
            last_name=shop_client.user.last_name,
            username=shop_client.user.username,
        ),
        has_gift=shop_client.has_gift,
        total_purchases_count=total_purchases_count,
        free_purchases_count=free_purchases_count,
        current_cups_count=current_cups_count,
    )


def get_clients_purchases_statistics(
        shop_id: int,
) -> list[ClientPurchasesStatistics]:
    return (
        ShopSale.objects
        .select_related('client__user')
        .filter(shop_id=shop_id)
        .values('client_id')
        .annotate(
            total_purchases_count=Count('id'),
            free_purchases_count=Count(
                Case(
                    When(
                        is_free=True,
                        then=1,
                    ),
                    output_field=IntegerField(),
                )
            )
        )
    )


def get_shop_client_statistics_list(
        shop: Shop,
) -> list[ShopClientStatistics]:
    clients = (
        ShopClient.objects
        .select_related('user')
        .filter(shop_id=shop.id)
        .values('id', 'user_id', 'user__first_name', 'user__last_name',
                'user__username', 'has_gift')
    )
    clients_purchases_statistics = get_clients_purchases_statistics(shop.id)
    client_id_to_purchases_statistics = {
        client_purchases_statistics['client_id']: client_purchases_statistics
        for client_purchases_statistics in clients_purchases_statistics
    }

    all_clients_statistics: list[ShopClientStatistics] = []
    for client in clients:
        purchases_statistics = client_id_to_purchases_statistics.get(
            client['id'],
            {'total_purchases_count': 0, 'free_purchases_count': 0},
        )
        total_purchases_count = purchases_statistics['total_purchases_count']
        free_purchases_count = purchases_statistics['free_purchases_count']
        current_cups_count = total_purchases_count % shop.each_nth_sale_free
        all_clients_statistics.append(
            ShopClientStatistics(
                client_id=client['id'],
                user=ClientUser(
                    id=client['user_id'],
                    first_name=client['user__first_name'],
                    last_name=client['user__last_name'],
                    username=client['user__username'],
                ),
                has_gift=client['has_gift'],
                total_purchases_count=total_purchases_count,
                free_purchases_count=free_purchases_count,
                current_cups_count=current_cups_count,
            )
        )

    return all_clients_statistics
