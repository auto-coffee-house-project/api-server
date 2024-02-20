from django.urls import include, path

from shops.views import (
    MailingCreateApi, SaleTemporaryCodeCreateApi, SalesmanInvitationCreateApi,
    ShopClientStatisticsListApi, ShopClientStatisticsRetrieveApi,
    ShopGroupGiftPhotoUpdateApi, ShopGroupRetrieveUpdateApi,
    ShopSaleCreateByCodeApi, ShopSaleCreateByUserIdApi, ShopSaleDeleteApi,
    ShopSalesmanListCreateDeleteApi,
)
from shops.views.shop_products import (
    ShopProductListCreateApi,
    ShopProductPhotoUpdateApi,
    ShopProductRetrieveUpdateDeleteApi,
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
    path(
        r'products/<int:product_id>/photos/',
        ShopProductPhotoUpdateApi.as_view(),
        name='product-photo-update',
    ),
    path(
        r'products/<int:product_id>/',
        ShopProductRetrieveUpdateDeleteApi.as_view(),
        name='product-retrieve-update-delete',
    ),
    path(
        r'products/',
        ShopProductListCreateApi.as_view(),
        name='product-list-create',
    ),
    path(r'clients/', include(clients_urlpatterns)),
    path(
        r'salesmans/',
        ShopSalesmanListCreateDeleteApi.as_view(),
        name='salesman-list-create-delete',
    ),
    path(r'sales/', include(sales_urlpatterns)),
    path(
        r'codes/',
        SaleTemporaryCodeCreateApi.as_view(),
        name='sale-temporary-code-create',
    ),
    path(
        r'groups/me/gift-photos/',
        ShopGroupGiftPhotoUpdateApi.as_view(),
    ),
    path(
        r'groups/bots/<int:bot_id>/',
        ShopGroupRetrieveUpdateApi.as_view(),
        name='group-retrieve',
    ),
    path(
        r'invitations/',
        SalesmanInvitationCreateApi.as_view(),
        name='invitation-create',
    ),
    path(
        r'mailings/',
        MailingCreateApi.as_view(),
        name='mailing-create',
    ),
]
