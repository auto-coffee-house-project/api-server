from django.urls import path

from shops.views import ShopSaleListCreateApi

urlpatterns = [
    path(r'sales/', ShopSaleListCreateApi.as_view()),
]
