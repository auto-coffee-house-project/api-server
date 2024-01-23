from rest_framework import serializers

from shops.models import ShopSalesman

__all__ = ('ShopSalesmanSerializer',)


class ShopSalesmanSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopSalesman
        fields = '__all__'
