from django.urls import path

from shops.views import (
    ShopSaleCreateApi,
    SaleTemporaryCodeCreateApi,
    ShopSalesmanRetrieveApi,
    ShopSaleDeleteApi,
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
        r'salesmans/<int:salesman_id>/',
        ShopSalesmanRetrieveApi.as_view(),
        name='salesman-retrieve',
    ),
]
