from rest_framework import serializers

__all__ = (
    'SegregationOptionsSerializer',
    'SegregationByBirthdaysSerializer',
    'ButtonSerializer',
    'SegregationByPurchasesSerializer',
)


class FromDateAndToDateSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()

    def validate(self, attrs):
        if attrs['from_date'] > attrs['to_date']:
            raise serializers.ValidationError(
                '"from_date" should be less than "to_date"'
            )
        return attrs


class SegregationByBirthdaysSerializer(FromDateAndToDateSerializer):
    pass


class SegregationByPurchasesSerializer(FromDateAndToDateSerializer):
    purchases_count = serializers.IntegerField(min_value=1)


class SegregationOptionsSerializer(serializers.Serializer):
    by_birthdays = SegregationByBirthdaysSerializer(required=False)
    by_purchases = SegregationByPurchasesSerializer(required=False)


class ButtonSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=64)
    url = serializers.URLField()
