from django.urls import path, include

from shops.views import (
    ShopSaleCreateByUserIdApi,
    ShopSaleCreateByCodeApi,
    SaleTemporaryCodeCreateApi,
    ShopSaleDeleteApi,
    ShopGroupRetrieveApi,
    SalesmanInvitationCreateApi,
    ShopAdminRetrieveApi,
    MailingCreateApi,
    ShopSalesmanListCreateApi,
    ShopClientStatisticsRetrieveApi,
    ShopClientStatisticsListApi,
)

sales_urlpatterns = [
    path(
        r'by-codes/',
        ShopSaleCreateByCodeApi.as_view(),
        name='sale-create-by-code',
    ),
    path(
        r'by-users/',
        ShopSaleCreateByUserIdApi.as_view(),
        name='sale-create-by-user-id',
    ),
    path(
        r'<int:sale_id>/',
        ShopSaleDeleteApi.as_view(),
        name='sale-delete',
    ),
]

clients_urlpatterns = [
    path(
        r'statistics/',
        ShopClientStatisticsRetrieveApi.as_view(),
        name='client-statistics',
    ),
    path(
        r'all-statistics/',
        ShopClientStatisticsListApi.as_view(),
        name='all-clients-statistics',
    )
]

urlpatterns = [
    path(r'clients/', include(clients_urlpatterns)),
    path(
        r'salesmans/',
        ShopSalesmanListCreateApi.as_view(),
        name='salesman-list-create',
    ),
    path(r'sales/', include(sales_urlpatterns)),
    path(
        r'codes/',
        SaleTemporaryCodeCreateApi.as_view(),
        name='sale-temporary-code-create',
    ),
    path(
        r'groups/bots/<int:bot_id>/',
        ShopGroupRetrieveApi.as_view(),
        name='group-retrieve',
    ),
    path(
        r'invitations/',
        SalesmanInvitationCreateApi.as_view(),
        name='invitation-create',
    ),
    path(
        r'admins/<int:user_id>/',
        ShopAdminRetrieveApi.as_view(),
        name='admin-retrieve',
    ),
    path(
        r'mailings/',
        MailingCreateApi.as_view(),
        name='mailing-create',
    ),
]
