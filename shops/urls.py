from django.urls import path, include

from shops.views import (
    ShopSaleCreateApi,
    SaleTemporaryCodeCreateApi,
    ShopSalesmanRetrieveDeleteApi,
    ShopSaleDeleteApi,
    ShopGroupRetrieveApi,
    SalesmanInvitationCreateApi,
    ShopAdminRetrieveApi,
    MailingCreateApi,
    ShopSalesmanListCreateApi,
    ShopClientStatisticsRetrieveApi,
)

salesmans_urlpatterns = [
    path(
        r'<int:user_id>/',
        ShopSalesmanRetrieveDeleteApi.as_view(),
        name='salesman-retrieve-delete',
    ),
    path(
        r'',
        ShopSalesmanListCreateApi.as_view(),
        name='salesman-list-create',
    )
]

sales_urlpatterns = [
    path(r'', ShopSaleCreateApi.as_view(), name='sale-create'),
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
]

urlpatterns = [
    path(r'clients/', include(clients_urlpatterns)),
    path(r'salesmans/', include(salesmans_urlpatterns)),
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
