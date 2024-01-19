from rest_framework.generics import ListCreateAPIView

from shops.models import ShopSale
from shops.serializers import ShopSaleSerializer

__all__ = ('ShopSaleListCreateApi',)


class ShopSaleListCreateApi(ListCreateAPIView):
    serializer_class = ShopSaleSerializer
    queryset = ShopSale.objects.all()
