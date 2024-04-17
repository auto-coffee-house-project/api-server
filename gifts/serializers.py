from rest_framework import serializers

__all__ = ('GiftSerializer',)


class GiftSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    code = serializers.CharField()
    is_main = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField()
