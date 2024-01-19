from rest_framework import serializers

from shops.models import ShopSale

__all__ = (
    'ShopSaleSerializer',
)


class ShopSaleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ShopSale
