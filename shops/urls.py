from django.urls import path

from shops.views import ShopSaleListCreateApi, SaleTemporaryCodeCreateApi

urlpatterns = [
    path(r'sales/', ShopSaleListCreateApi.as_view()),
    path(r'codes/', SaleTemporaryCodeCreateApi.as_view(), name='sale-code')
]
