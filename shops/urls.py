from django.urls import include, path

from shops.views import (
    EmployeeInvitationCreateApi,
    SaleCodeCreateApi,
    ShopClientListApi,
    ShopClientRetrieveApi,
    ShopEmployeeDeleteApi,
    ShopEmployeeListCreateApi,
    ShopRetrieveUpdateApi,
    ShopSaleCreateByCodeApi,
    ShopSaleCreateByUserIdApi,
    ShopSaleDeleteApi,
)
from shops.views.shop_products import (
    ShopProductListCreateApi,
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

products_urlpatterns = [
    path(
        r'<int:product_id>/',
        ShopProductRetrieveUpdateDeleteApi.as_view(),
        name='product-retrieve-update-delete',
    ),
    path(
        r'',
        ShopProductListCreateApi.as_view(),
        name='product-list-create',
    ),
]

employees_urlpatterns = [
    path(
        r'',
        ShopEmployeeListCreateApi.as_view(),
        name='employee-list-create',
    ),
    path(
        r'<int:employee_id>/',
        ShopEmployeeDeleteApi.as_view(),
        name='employee-delete',
    ),
]

clients_urlpatterns = [
    path(
        r'',
        ShopClientListApi.as_view(),
        name='client-list',
    ),
    path(
        r'users/<int:user_id>/',
        ShopClientRetrieveApi.as_view(),
        name='client-retrieve',
    ),
]

urlpatterns = [
    path(r'clients/', include(clients_urlpatterns)),
    path(r'products/', include(products_urlpatterns)),
    path(r'employees/', include(employees_urlpatterns)),
    path(r'sales/', include(sales_urlpatterns)),
    path(
        r'me/',
        ShopRetrieveUpdateApi.as_view(),
        name='group-retrieve',
    ),
    path(
        r'sale-codes/',
        SaleCodeCreateApi.as_view(),
        name='sale-code-create',
    ),
    path(
        r'invitations/',
        EmployeeInvitationCreateApi.as_view(),
        name='invitation-create',
    ),
]
