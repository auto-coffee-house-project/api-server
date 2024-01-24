from django.urls import path

from shops.views import (
    ShopSaleCreateApi,
    SaleTemporaryCodeCreateApi,
    ShopSalesmanRetrieveApi,
    ShopSaleDeleteApi,
    ShopGroupRetrieveApi,
    SalesmanInvitationCreateApi, ShopAdminRetrieveApi,
)

urlpatterns = [
    path(r'sales/', ShopSaleCreateApi.as_view(), name='sale-create'),
    path(r'sales/', ShopSaleDeleteApi.as_view(), name='sale-delete'),
    path(
        r'codes/',
        SaleTemporaryCodeCreateApi.as_view(),
        name='sale-temporary-code-create',
    ),
    path(
        r'salesmans/<int:user_id>/',
        ShopSalesmanRetrieveApi.as_view(),
        name='salesman-retrieve',
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
]
