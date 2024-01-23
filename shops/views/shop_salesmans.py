from rest_framework.generics import RetrieveAPIView

from shops.models import ShopSalesman
from shops.serializers import ShopSalesmanSerializer


class ShopSalesmanRetrieveApi(RetrieveAPIView):
    queryset = ShopSalesman.objects.all()
    serializer_class = ShopSalesmanSerializer
    lookup_url_kwarg = 'salesman_user_id'
    lookup_field = 'user_id'
